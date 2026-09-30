from model.Ativos import Ativo
from model.enuns.Categorias import Categoria


class Servidor(Ativo):

    def __init__(self, id, nome, responsavel, setor, localizacao, vulnerabilidades):
        super().__init__(id, nome, Categoria.servidor, responsavel, setor, localizacao, vulnerabilidades)
