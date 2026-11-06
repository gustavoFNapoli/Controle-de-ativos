import math
import sys

from model.AtivoFactory import AtivoFactory
from repository.AnaliseDeRiscoRepository import AnaliseDeRiscoRepository
from utils.Ferramentas import Ferramentas


class AnaliseDeRiscoService:
    LIMITE_CONDICIONAMENTO = 1e12

    def __init__(self):
        self.repository = AnaliseDeRiscoRepository()

    @staticmethod
    def _inverter(matriz):
        tamanho = len(matriz)
        identidade = [
            [1.0 if linha == coluna else 0.0 for coluna in range(tamanho)]
            for linha in range(tamanho)
        ]
        ampliada = [
            [float(valor) for valor in linha] + identidade[indice]
            for indice, linha in enumerate(matriz)
        ]
        norma = max(
            (sum(abs(valor) for valor in linha) for linha in matriz),
            default=0.0,
        )
        tolerancia = sys.float_info.epsilon * max(1, tamanho) * max(1.0, norma)

        for coluna in range(tamanho):
            pivo = max(
                range(coluna, tamanho),
                key=lambda linha: abs(ampliada[linha][coluna]),
            )
            if abs(ampliada[pivo][coluna]) <= tolerancia:
                raise ValueError("A matriz I - A não é invertível.")
            ampliada[coluna], ampliada[pivo] = ampliada[pivo], ampliada[coluna]

            divisor = ampliada[coluna][coluna]
            ampliada[coluna] = [valor / divisor for valor in ampliada[coluna]]
            for linha in range(tamanho):
                if linha == coluna:
                    continue
                fator = ampliada[linha][coluna]
                ampliada[linha] = [
                    valor - fator * pivo_valor
                    for valor, pivo_valor in zip(
                        ampliada[linha], ampliada[coluna]
                    )
                ]

        return [linha[tamanho:] for linha in ampliada]

    @staticmethod
    def _resolver(matriz, vetor):
        tamanho = len(vetor)
        ampliada = [
            [float(valor) for valor in matriz[linha]] + [float(vetor[linha])]
            for linha in range(tamanho)
        ]

        for coluna in range(tamanho):
            pivo = max(
                range(coluna, tamanho),
                key=lambda linha: abs(ampliada[linha][coluna]),
            )
            if ampliada[pivo][coluna] == 0:
                raise ValueError("A matriz I - A não é invertível.")
            ampliada[coluna], ampliada[pivo] = ampliada[pivo], ampliada[coluna]

            for linha in range(coluna + 1, tamanho):
                fator = ampliada[linha][coluna] / ampliada[coluna][coluna]
                for indice in range(coluna, tamanho + 1):
                    ampliada[linha][indice] -= fator * ampliada[coluna][indice]

        solucao = [0.0] * tamanho
        for linha in range(tamanho - 1, -1, -1):
            restante = ampliada[linha][tamanho] - sum(
                ampliada[linha][coluna] * solucao[coluna]
                for coluna in range(linha + 1, tamanho)
            )
            solucao[linha] = restante / ampliada[linha][linha]
        return solucao

    @staticmethod
    def _norma_infinito(matriz):
        return max(
            (sum(abs(valor) for valor in linha) for linha in matriz),
            default=0.0,
        )

    def _calcular(self, ativos_model, vulnerabilidades, vinculos, dependencias):
        ativos = [AtivoFactory.from_ativo_model(model) for model in ativos_model]
        indices_ativos = {model.id: indice for indice, model in enumerate(ativos_model)}
        indices_vulnerabilidades = {
            model.id: indice for indice, model in enumerate(vulnerabilidades)
        }
        quantidade_ativos = len(ativos)
        vetor_severidade = []

        for vulnerabilidade in vulnerabilidades:
            nota = float(vulnerabilidade.cvss_score or 0)
            if not math.isfinite(nota) or not 0 <= nota <= 10:
                raise ValueError(
                    f"A nota CVSS da vulnerabilidade {vulnerabilidade.id} "
                    "deve estar entre 0 e 10."
                )
            vetor_severidade.append(nota)

        matriz_incidencia = [
            [0 for _ in vulnerabilidades] for _ in range(quantidade_ativos)
        ]
        for vinculo in vinculos:
            indice_ativo = indices_ativos.get(vinculo.id_ativo)
            indice_vulnerabilidade = indices_vulnerabilidades.get(
                vinculo.id_vulnerabilidade
            )
            if indice_ativo is not None and indice_vulnerabilidade is not None:
                matriz_incidencia[indice_ativo][indice_vulnerabilidade] = 1
        risco_proprio = [
            sum(
                incidencias[coluna] * vetor_severidade[coluna]
                for coluna in range(len(vetor_severidade))
            )
            for incidencias in matriz_incidencia
        ]

        matriz_dependencias = [
            [0.0 for _ in range(quantidade_ativos)]
            for _ in range(quantidade_ativos)
        ]
        for dependencia in dependencias:
            indice_destino = indices_ativos.get(dependencia.id_ativo)
            indice_origem = indices_ativos.get(dependencia.id_dependencia)
            fracao = float(dependencia.fracao)
            if indice_destino is None or indice_origem is None:
                continue
            if indice_destino == indice_origem or not 0 <= fracao < 1:
                raise ValueError("Foi encontrada uma dependência inválida.")
            matriz_dependencias[indice_destino][indice_origem] = fracao

        if any(sum(linha) >= 1 for linha in matriz_dependencias):
            raise ValueError(
                "A soma das frações de dependência de cada ativo deve ser menor que 1."
            )

        if not quantidade_ativos:
            return [], 1.0

        sistema = [
            [
                (1.0 if linha == coluna else 0.0)
                - matriz_dependencias[linha][coluna]
                for coluna in range(quantidade_ativos)
            ]
            for linha in range(quantidade_ativos)
        ]
        inversa = self._inverter(sistema)
        numero_condicao = (
            self._norma_infinito(sistema) * self._norma_infinito(inversa)
        )
        if not math.isfinite(numero_condicao) or (
            numero_condicao > self.LIMITE_CONDICIONAMENTO
        ):
            raise ValueError(
                "O sistema está mal condicionado e sua solução não é confiável "
                f"(número de condição: {numero_condicao:.3g})."
            )

        risco_efetivo = self._resolver(sistema, risco_proprio)
        resultado = [
            {
                "ativo": ativo,
                "risco_proprio": risco_proprio[indice],
                "risco_efetivo": risco_efetivo[indice],
                "quantidade_vulnerabilidades": sum(
                    1 for vinculo in vinculos
                    if vinculo.id_ativo == ativos_model[indice].id
                ),
            }
            for indice, ativo in enumerate(ativos)
        ]
        return resultado, numero_condicao

    def calcular(self):
        try:
            ativos_model, vulnerabilidades, vinculos, dependencias = (
                self.repository.carregar_dados()
            )
            riscos, numero_condicao = self._calcular(
                ativos_model, vulnerabilidades, vinculos, dependencias
            )
            ativos_por_id = {
                ativo.getId(): ativo.getNome()
                for ativo in (
                    AtivoFactory.from_ativo_model(model)
                    for model in ativos_model
                )
            }
            dependencias_view = [
                {
                    "id_ativo": item.id_ativo,
                    "id_dependencia": item.id_dependencia,
                    "fracao": item.fracao,
                    "nome_ativo": ativos_por_id[item.id_ativo],
                    "nome_dependencia": ativos_por_id[item.id_dependencia],
                }
                for item in dependencias
            ]
            return Ferramentas.resultado(
                True,
                "Riscos calculados.",
                {
                    "riscos": riscos,
                    "dependencias": dependencias_view,
                    "numero_condicao": numero_condicao,
                    "ativos": [
                        AtivoFactory.from_ativo_model(ativo)
                        for ativo in ativos_model
                    ],
                },
            )
        except (ValueError, ArithmeticError) as erro:
            return Ferramentas.resultado(False, str(erro))
        except Exception as erro:
            return Ferramentas.resultado(
                False, f"Falha ao calcular os riscos: {erro}"
            )

    def salvar_dependencia(self, formulario):
        try:
            id_ativo = int(formulario.get("id_ativo"))
            id_dependencia = int(formulario.get("id_dependencia"))
            fracao = float(formulario.get("fracao"))
            if not math.isfinite(fracao):
                raise ValueError
            sucesso, mensagem = self.repository.salvar_dependencia(
                id_ativo, id_dependencia, fracao
            )
            return Ferramentas.resultado(sucesso, mensagem)
        except (TypeError, ValueError):
            return Ferramentas.resultado(
                False, "Informe ativos válidos e uma fração numérica entre 0 e 1."
            )
        except Exception as erro:
            return Ferramentas.resultado(
                False, f"Falha ao salvar a dependência: {erro}"
            )

    def remover_dependencia(self, formulario):
        try:
            removida = self.repository.remover_dependencia(
                int(formulario.get("id_ativo")),
                int(formulario.get("id_dependencia")),
            )
            if not removida:
                return Ferramentas.resultado(False, "Dependência não encontrada.")
            return Ferramentas.resultado(True, "Dependência removida.")
        except (TypeError, ValueError):
            return Ferramentas.resultado(False, "Dependência informada inválida.")
        except Exception as erro:
            return Ferramentas.resultado(
                False, f"Falha ao remover a dependência: {erro}"
            )
