from model.enuns.Categorias import Categoria

class Ativo:
    def __init__(self, id, nome, categoria, responsavel, setor, localizacao, vulnerabilidades):
        self.id = id
        self.nome = nome
        self.categoria = Categoria(categoria)
        self.responsavel = responsavel
        self.setor = setor
        self.localizacao = localizacao
        self.vulnerabilidades = vulnerabilidades
