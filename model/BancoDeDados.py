from model.Ativos import Ativo
from model.enuns.Categorias import Categoria


class BancoDeDados(Ativo):
    def __init__(self, id, nome, responsavel, setor, localizacao, vulnerabilidades):
        super().__init__(id, nome, Categoria.banco_de_dados, responsavel, setor, localizacao, vulnerabilidades)
