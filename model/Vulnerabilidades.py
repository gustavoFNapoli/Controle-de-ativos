from model.enuns.Severidade import Severidade


class Vulnerabilidade:
    def __init__(self, vulnerabilidade, severidade):
        self.vulnerabilidade = vulnerabilidade
        self.severidade = Severidade(severidade)
