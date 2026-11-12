from model.Ativos import Ativo
from model.enuns.Categorias import Categoria


class Servidor(Ativo):
    fator_transmissao_risco = 0.8

    def __init__(self, id, nome, responsavel, setor, localizacao):
        super().__init__(id, nome, Categoria.servidor, responsavel, setor, localizacao)
