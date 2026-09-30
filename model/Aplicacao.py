from model.Ativos import Ativo
from model.enuns.Categorias import Categoria


class Aplicacao(Ativo):

    def __init__(self, id, nome, responsavel, setor, localizacao, vulnerabilidades):
        super().__init__(id, nome, Categoria.aplicacao, responsavel, setor, localizacao, vulnerabilidades)

