import math

import numpy as np

from model.AtivoFactory import AtivoFactory
from repository.AnaliseDeRiscoRepository import AnaliseDeRiscoRepository
from utils.Ferramentas import Ferramentas


class AnaliseDeRiscoService:
    LIMITE_CONDICIONAMENTO = 1e12

    def __init__(self):
        self.repository = AnaliseDeRiscoRepository()

    @staticmethod
    def _validar_sistema(matriz):
        try:
            sinal, log_determinante = np.linalg.slogdet(matriz)
        except np.linalg.LinAlgError as erro:
            raise ValueError("Não foi possível verificar a matriz I - A.") from erro
        if sinal == 0 or not np.isfinite(log_determinante):
            raise ValueError("A matriz I - A não é invertível.")

        try:
            numero_condicao = float(np.linalg.cond(matriz))
        except np.linalg.LinAlgError as erro:
            raise ValueError(
                "Não foi possível avaliar o condicionamento da matriz I - A."
            ) from erro
        if not math.isfinite(numero_condicao) or (
            numero_condicao > AnaliseDeRiscoService.LIMITE_CONDICIONAMENTO
        ):
            raise ValueError(
                "O sistema está mal condicionado e sua solução não é confiável "
                f"(número de condição: {numero_condicao:.3g})."
            )
        return numero_condicao

    @staticmethod
    def _vetor_severidade(vulnerabilidades):
        vetor = np.zeros(len(vulnerabilidades), dtype=float)

        for indice, vulnerabilidade in enumerate(vulnerabilidades):
            nota = float(vulnerabilidade.cvss_score or 0)
            if not math.isfinite(nota) or not 0 <= nota <= 10:
                raise ValueError(
                    f"A nota CVSS da vulnerabilidade {vulnerabilidade.id} "
                    "deve estar entre 0 e 10."
                )
            vetor[indice] = nota

        return vetor

    @staticmethod
    def _matriz_incidencia(quantidade_ativos,
                           vulnerabilidades,
                           vinculos,
                           indices_ativos,
                           indices_vulnerabilidades):
        matriz = np.zeros(
            (quantidade_ativos, len(vulnerabilidades)), dtype=float
        )
        for vinculo in vinculos:
            indice_ativo = indices_ativos.get(vinculo.id_ativo)
            indice_vulnerabilidade = indices_vulnerabilidades.get(
                vinculo.id_vulnerabilidade
            )
            if indice_ativo is not None and indice_vulnerabilidade is not None:
                matriz[indice_ativo][indice_vulnerabilidade] = 1

        return matriz

    @staticmethod
    def _matriz_dependencias(
        quantidade_ativos,
        indices_ativos,
        dependencias,
        fatores_transmissao,
    ):
        matriz = np.zeros(
            (quantidade_ativos, quantidade_ativos), dtype=float
        )
        for dependencia in dependencias:
            indice_destino = indices_ativos.get(dependencia.id_ativo)
            indice_origem = indices_ativos.get(dependencia.id_dependencia)
            if indice_destino is None or indice_origem is None:
                continue
            fracao = float(fatores_transmissao[dependencia.id_ativo])
            if (
                indice_destino == indice_origem
                or not math.isfinite(fracao)
                or not 0 <= fracao < 1
            ):
                raise ValueError("Foi encontrada uma dependência inválida.")
            matriz[indice_destino][indice_origem] = fracao

        if np.any(np.sum(matriz, axis=1) >= 1):
            raise ValueError(
                "A soma das frações de dependência de cada ativo deve ser menor que 1."
            )
        return matriz

    def _calcular_riscos(self, ativos_model, vulnerabilidades, vinculos, dependencias):
        ativos = [AtivoFactory.from_ativo_model(model) for model in ativos_model]
        indices_ativos = {model.id: indice for indice, model in enumerate(ativos_model)}
        fatores_transmissao = {
            ativo.getId(): ativo.getFatorTransmissaoRisco() for ativo in ativos
        }
        indices_vulnerabilidades = {
            model.id: indice for indice, model in enumerate(vulnerabilidades)
        }
        quantidade_ativos = len(ativos)
        vetor_severidade = self._vetor_severidade(vulnerabilidades)

        matriz_incidencia = self._matriz_incidencia(
            quantidade_ativos,
            vulnerabilidades,
            vinculos,
            indices_ativos,
            indices_vulnerabilidades,
        )

        risco_proprio = matriz_incidencia @ vetor_severidade

        matriz_dependencias = self._matriz_dependencias(
            quantidade_ativos,
            indices_ativos,
            dependencias,
            fatores_transmissao,
        )

        if not quantidade_ativos:
            return [], 1.0

        sistema = np.eye(quantidade_ativos) - matriz_dependencias
        numero_condicao = self._validar_sistema(sistema)
        try:
            risco_efetivo = np.linalg.solve(sistema, risco_proprio)
        except np.linalg.LinAlgError as erro:
            raise ValueError("A matriz I - A não é invertível.") from erro
        resultado = [
            {
                "ativo": ativo,
                "risco_proprio": float(risco_proprio[indice]),
                "risco_efetivo": float(risco_efetivo[indice]),
                "quantidade_vulnerabilidades": int(
                    np.count_nonzero(matriz_incidencia[indice])
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
            riscos, numero_condicao = self._calcular_riscos(
                ativos_model, vulnerabilidades, vinculos, dependencias
            )
            ativos = [
                AtivoFactory.from_ativo_model(model) for model in ativos_model
            ]
            ativos_por_id = {ativo.getId(): ativo for ativo in ativos}
            dependencias_view = [
                {
                    "id_ativo": item.id_ativo,
                    "id_dependencia": item.id_dependencia,
                    "fracao": ativos_por_id[
                        item.id_ativo
                    ].getFatorTransmissaoRisco(),
                    "nome_ativo": ativos_por_id[item.id_ativo].getNome(),
                    "nome_dependencia": ativos_por_id[
                        item.id_dependencia
                    ].getNome(),
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
                    "ativos": ativos,
                },
            )
        except (ValueError, ArithmeticError, np.linalg.LinAlgError) as erro:
            return Ferramentas.resultado(False, str(erro))
        except Exception as erro:
            return Ferramentas.resultado(
                False, f"Falha ao calcular os riscos: {erro}"
            )

    def salvar_dependencia(self, formulario):
        try:
            id_ativo = int(formulario.get("id_ativo"))
            id_dependencia = int(formulario.get("id_dependencia"))
            sucesso, mensagem = self.repository.salvar_dependencia(
                id_ativo, id_dependencia
            )
            return Ferramentas.resultado(sucesso, mensagem)
        except (TypeError, ValueError):
            return Ferramentas.resultado(
                False, "Selecione ativos válidos para criar a dependência."
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
