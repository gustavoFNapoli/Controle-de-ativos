from model.Vulnerabilidades import Vulnerabilidade
from model.enuns.Categorias import Categoria

class Ativo:
    def __init__(self, nome, categoria:Categoria, responsavel, setor, localizacao, vulnerabilidades):
        self.nome = nome
        self.categoria = categoria
        self.responsavel = responsavel
        self.setor = setor
        self.localizacao = localizacao
        self.vulnerabilidades = vulnerabilidades

    def adicionar_vulnerabilidade(self, vulnerabilidade: Vulnerabilidade):
        self.vulnerabilidades['lista'].append(vulnerabilidade.to_json())