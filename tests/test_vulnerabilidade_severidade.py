import unittest

from model.VulnerabilidadeFactory import VulnerabilidadeFactory
from model.enuns.Severidade import Severidade
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel


class VulnerabilidadeSeveridadeTest(unittest.TestCase):
    def test_cvss_define_severidade_nos_limites_das_faixas(self):
        casos = [
            (0, Severidade.baixa),
            (2.9, Severidade.baixa),
            (3, Severidade.media),
            (5.9, Severidade.media),
            (6, Severidade.alta),
            (8.9, Severidade.alta),
            (9, Severidade.critica),
            (10, Severidade.critica),
        ]

        for nota, severidade_esperada in casos:
            with self.subTest(nota=nota):
                vulnerabilidade = VulnerabilidadeFactory.gerar_vulnerabilidade(
                    "Falha de teste",
                    "1",
                    "2",
                    str(nota),
                )
                self.assertIsNotNone(vulnerabilidade)
                self.assertEqual(
                    severidade_esperada,
                    vulnerabilidade.getSeveridade(),
                )

    def test_leitura_usa_cvss_mesmo_se_severidade_salva_estiver_desatualizada(self):
        registro = VulnerabilidadeModel(
            id=1,
            vulnerabilidade="Falha de teste",
            severidade=1,
            cvss_score=9,
            tipo=1,
            status=2,
        )

        vulnerabilidade = (
            VulnerabilidadeFactory.from_vulnerabilidade_model(registro)
        )

        self.assertEqual(Severidade.critica, vulnerabilidade.getSeveridade())

    def test_rejeita_nota_cvss_fora_do_intervalo(self):
        for nota in ("-0.1", "10.1", "nan", "inf"):
            with self.subTest(nota=nota):
                self.assertIsNone(
                    VulnerabilidadeFactory.gerar_vulnerabilidade(
                        "Falha de teste",
                        "1",
                        "2",
                        nota,
                    )
                )


if __name__ == "__main__":
    unittest.main()
