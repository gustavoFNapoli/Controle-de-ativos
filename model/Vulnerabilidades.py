from model.enuns.Severidade import Severidade
from model.enuns.Status import Status
from model.enuns.TiposVulnerabilidade import Tipo


class Vulnerabilidade:
    def __init__(self, vulnerabilidade, severidade:Severidade, tipo:Tipo, status:Status):
        self.vulnerabilidade = vulnerabilidade
        self.severidade = severidade
        self.tipo = tipo
        self.status = status

    def to_json(self):
        return {"vulnerabilidade": self.vulnerabilidade,
                "severidade": self.severidade.name,
                "tipo": self.tipo.name,
                "status": self.status.name}