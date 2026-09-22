from enum import Enum

class Categoria(Enum):
    servidor = 'servidor'
    software_licenciado = 'software_licenciado'
    banco_de_dados = 'banco_de_dados'
    aplicacao = 'aplicacao'
    equipamento = 'equipamento'

    def get_by_number(numero:int):
        for item in Categoria:
            if item.value == numero:
                return item
        return None