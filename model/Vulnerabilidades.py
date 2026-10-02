from model.enuns.Severidade import Severidade
from model.enuns.Status import Status
from model.enuns.TiposVulnerabilidade import Tipo
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel


class Vulnerabilidade:
    def __init__(self, id, vulnerabilidade, severidade, tipo, status):
        self.__id = id
        self.__vulnerabilidade = vulnerabilidade
        self.__severidade = Severidade.get_by_number(int(severidade))
        self.__tipo = Tipo.get_by_number(int(tipo))
        self.__status = Status.get_by_number(int(status))

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

    def toVulnerabilidadeModel(self):
        return VulnerabilidadeModel(
            id = self.__id,
            vulnerabilidade = self.__vulnerabilidade,
            severidade = self.__severidade.value,
            tipo = self.__tipo.value,
            status = self.__status.value
        )

    @classmethod
    def fromVulnerabilidadeModel(cls, vulnerabilidade:VulnerabilidadeModel):
        return cls(
            id = vulnerabilidade.id,
            vulnerabilidade = vulnerabilidade.vulnerabilidade,
            severidade = vulnerabilidade.severidade,
            tipo = vulnerabilidade.tipo,
            status = vulnerabilidade.status
        )