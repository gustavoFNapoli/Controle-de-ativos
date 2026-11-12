from model.Ativos import Ativo
from model.enuns.Categorias import Categoria


class BancoDeDados(Ativo):
    fator_transmissao_risco = 0.7

    def __init__(self, id, nome, responsavel, setor, localizacao):
        super().__init__(id, nome, Categoria.banco_de_dados, responsavel, setor, localizacao)
