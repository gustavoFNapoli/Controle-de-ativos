from model.Ativos import Ativo
from model.enuns.Categorias import Categoria


class Equipamento(Ativo):
    fator_transmissao_risco = 0.3

    def __init__(self, id, nome, responsavel, setor, localizacao):
        super().__init__(id, nome, Categoria.equipamento, responsavel, setor, localizacao)
