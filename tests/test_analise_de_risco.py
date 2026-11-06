import unittest

from repository.models.AtivoModel import AtivoModel
from repository.models.DependenciaAtivoModel import DependenciaAtivoModel
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel
from repository.models.VulnerabilidadesAtivosModel import VulnerabilidadesAtivos
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
            DependenciaAtivoModel(
                id_ativo=3, id_dependencia=2, fracao=0.25,
            ),
        ]

        riscos, condicao = self.service._calcular(
            self.ativos, vulnerabilidades, vinculos, dependencias
        )

        self.assertEqual([4, 2, 0], [item["risco_proprio"] for item in riscos])
        self.assertEqual([4, 4, 1], [item["risco_efetivo"] for item in riscos])
        self.assertGreaterEqual(condicao, 1)

    def test_rejeita_sistema_singular(self):
        with self.assertRaisesRegex(ValueError, "não é invertível"):
            self.service._inverter([[0.0, 0.0], [0.0, 1.0]])

    def test_rejeita_dependencias_com_soma_unitaria(self):
        with self.assertRaisesRegex(ValueError, "menor que 1"):
            self.service._calcular(
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
            self.service._calcular(
                self.ativos[:2],
                [],
                [],
                [
                    DependenciaAtivoModel(
                        id_ativo=1, id_dependencia=2,
                        fracao=0.9999999999999,
                    ),
                    DependenciaAtivoModel(
                        id_ativo=2,
                        id_dependencia=1,
                        fracao=0.9999999999999,
                    )
                ],
            )


if __name__ == "__main__":
    unittest.main()
