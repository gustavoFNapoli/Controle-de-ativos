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
                status
            )
        except Exception as e:
            return None

    @staticmethod
    def gerar_vulnerabilidade(vulnerabilidade, severidade, tipo, status, id = None):
        try:
            severidadeplus = Severidade.get_by_number(int(severidade))
            tipoplus = Tipo.get_by_number(int(tipo))
            statusplus = Status.get_by_number(int(status))

            return Vulnerabilidade(
                id,
                vulnerabilidade,
                severidadeplus,
                tipoplus,
                statusplus
            )
        except Exception as e:
            return None
