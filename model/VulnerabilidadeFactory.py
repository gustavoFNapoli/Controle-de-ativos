from model.Vulnerabilidades import Vulnerabilidade
from model.enuns.Severidade import Severidade
from model.enuns.Status import Status
from model.enuns.TiposVulnerabilidade import Tipo
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel


class VulnerabilidadeFactory:

    @staticmethod
    def from_vulnerabilidade_model(vulnerabilidade:VulnerabilidadeModel):
        try:
            severidade = Severidade.get_by_number(int(vulnerabilidade.severidade))
            tipo = Tipo.get_by_number(int(vulnerabilidade.tipo))
            status = Status.get_by_number(int(vulnerabilidade.status))

            return Vulnerabilidade(
                vulnerabilidade.id,
                vulnerabilidade.vulnerabilidade,
                severidade,
                tipo,
                status,
                vulnerabilidade.cvss_score
            )
        except Exception as e:
            return None

    @staticmethod
    def gerar_vulnerabilidade(
        vulnerabilidade,
        severidade,
        tipo,
        status,
        cvss_score,
        id=None,
    ):
        try:
            if (
                not vulnerabilidade
                or not vulnerabilidade.strip()
                or len(vulnerabilidade.strip()) > 255
            ):
                return None
            cvss_score = float(cvss_score)
            if not 0 <= cvss_score <= 10:
                return None
            severidadeplus = Severidade.get_by_number(int(severidade))
            tipoplus = Tipo.get_by_number(int(tipo))
            statusplus = Status.get_by_number(int(status))
            if severidadeplus is None or tipoplus is None or statusplus is None:
                return None

            return Vulnerabilidade(
                id,
                vulnerabilidade,
                severidadeplus,
                tipoplus,
                statusplus,
                cvss_score,
            )
        except (TypeError, ValueError):
            return None
