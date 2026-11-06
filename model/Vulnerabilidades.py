from model.enuns.Severidade import Severidade
from model.enuns.Status import Status
from model.enuns.TiposVulnerabilidade import Tipo
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel


class Vulnerabilidade:
    def __init__(
        self,
        id,
        vulnerabilidade,
        severidade: Severidade,
        tipo: Tipo,
        status: Status,
        cvss_score=0,
    ):
        self.__id = id
        self.__vulnerabilidade = vulnerabilidade
        self.__severidade = severidade
        self.__tipo = tipo
        self.__status = status
        self.__cvss_score = float(cvss_score)

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id = id

    def getVulnerabilidade(self):
        return self.__vulnerabilidade

    def setVulnerabilidade(self, vulnerabilidade):
        self.__vulnerabilidade = vulnerabilidade

    def getSeveridade(self):
        return self.__severidade

    def setSeveridade(self, severidade):
        self.__severidade = Severidade.get_by_number(int(severidade))

    def getTipo(self):
        return self.__tipo

    def setTipo(self, tipo):
        self.__tipo = Tipo.get_by_number(int(tipo))

    def getStatus(self):
        return self.__status

    def setStatus(self, status):
        self.__status = Status.get_by_number(int(status))

    def getCVSSScore(self):
        return self.__cvss_score

    def setCVSSScore(self, score):
        self.__cvss_score = float(score)

    def toVulnerabilidadeModel(self):
        return VulnerabilidadeModel(
            id = self.__id,
            vulnerabilidade = self.__vulnerabilidade,
            severidade = self.__severidade.value,
            cvss_score = self.__cvss_score,
            tipo = self.__tipo.value,
            status = self.__status.value
        )