from model.enuns.Severidade import Severidade
from model.enuns.Status import Status
from model.enuns.TiposVulnerabilidade import Tipo


class Vulnerabilidade:
    def __init__(self, vulnerabilidade, severidade, tipo:Tipo, status:Status):
        self.vulnerabilidade = vulnerabilidade
        self.severidade = Severidade(severidade)
        self.tipo = tipo
        self.status = status

    def to_json(self):
        return {"vulnerabilidade": self.vulnerabilidade, "severidade": self.severidade, "tipo": self.tipo, "status": self.status}