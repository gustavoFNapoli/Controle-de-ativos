import unittest

import numpy as np

from repository.models.AtivoModel import AtivoModel
from repository.models.DependenciaAtivoModel import DependenciaAtivoModel
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel
from repository.models.VulnerabilidadesAtivosModel import VulnerabilidadesAtivos
from model.AtivoFactory import AtivoFactory
from service.AnaliseDeRiscoService import AnaliseDeRiscoService


class AnaliseDeRiscoTest(unittest.TestCase):
    def setUp(self):
        self.service = AnaliseDeRiscoService()
        self.ativos = [
            AtivoModel(
                id=1, nome="Servidor", categoria=1,
                responsavel="Equipe", setor="TI", localizacao="Sala 1",
            ),
            AtivoModel(
                id=2, nome="Aplicação", categoria=4,
                responsavel="Equipe", setor="TI", localizacao="Sala 2",
            ),
            AtivoModel(
                id=3, nome="Banco", categoria=3,
                responsavel="Equipe", setor="TI", localizacao="Sala 3",
            ),
        ]

    def test_risco_proprio_e_risco_herdado(self):
        vulnerabilidades = [
            VulnerabilidadeModel(
                id=1, vulnerabilidade="Vuln 1", severidade=3,
                cvss_score=4, tipo=1, status=2,
            ),
            VulnerabilidadeModel(
                id=2, vulnerabilidade="Vuln 2", severidade=2,
                cvss_score=2, tipo=1, status=2,
            ),
        ]
        vinculos = [
            VulnerabilidadesAtivos(id_ativo=1, id_vulnerabilidade=1),
            VulnerabilidadesAtivos(id_ativo=2, id_vulnerabilidade=2),
        ]
        dependencias = [
            DependenciaAtivoModel(
                id_ativo=2, id_dependencia=1, fracao=0.5,
            ),
            DependenciaAtivoModel(id_ativo=3, id_dependencia=2, fracao=0.25),
        ]

        riscos, condicao = self.service._calcular_riscos(
            self.ativos, vulnerabilidades, vinculos, dependencias
        )

        self.assertEqual([4, 2, 0], [item["risco_proprio"] for item in riscos])
        self.assertEqual([4, 4, 2.8], [item["risco_efetivo"] for item in riscos])
        self.assertGreaterEqual(condicao, 1)

    def test_fatores_de_transmissao_por_tipo_de_ativo(self):
        fatores_esperados = {
            1: 0.8,
            2: 0.5,
            3: 0.7,
            4: 0.5,
            5: 0.3,
        }

        for categoria, fator_esperado in fatores_esperados.items():
            with self.subTest(categoria=categoria):
                ativo = AtivoModel(
                    id=categoria,
                    nome=f"Ativo {categoria}",
                    categoria=categoria,
                    responsavel="Equipe",
                    setor="TI",
                    localizacao="Sala",
                )
                objeto_ativo = AtivoFactory.from_ativo_model(ativo)
                self.assertEqual(
                    fator_esperado,
                    objeto_ativo.getFatorTransmissaoRisco(),
                )

    def test_rejeita_sistema_singular(self):
        with self.assertRaisesRegex(ValueError, "não é invertível"):
            self.service._validar_sistema(np.array([[1.0, 1.0], [1.0, 1.0]]))

    def test_rejeita_dependencias_com_soma_unitaria(self):
        with self.assertRaisesRegex(ValueError, "menor que 1"):
            self.service._calcular_riscos(
                self.ativos,
                [],
                [],
                [
                    DependenciaAtivoModel(
                        id_ativo=1, id_dependencia=2, fracao=0.6,
                    ),
                    DependenciaAtivoModel(
                        id_ativo=1, id_dependencia=3, fracao=0.4,
                    ),
                ],
            )

    def test_rejeita_sistema_mal_condicionado(self):
        with self.assertRaisesRegex(ValueError, "mal condicionado"):
            self.service._validar_sistema(np.diag([1e-13, 1.0]))


if __name__ == "__main__":
    unittest.main()
