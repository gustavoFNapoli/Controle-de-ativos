from model.Ativos import Ativo
from model.enuns.Categorias import Categoria


class Software(Ativo):
    fator_transmissao_risco = 0.5

    def __init__(self, id, nome, responsavel, setor, localizacao):
        super().__init__(id, nome, Categoria.software_licenciado, responsavel, setor, localizacao)