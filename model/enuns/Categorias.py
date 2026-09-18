from enum import Enum

class Categoria(Enum):
    servidor = 1
    software_licencidado = 2
    banco_de_dados = 3
    aplicacao = 4
    equipamento = 5

    def get_by_number(numero):
        for item in Categoria:
            if item.value == numero:
                return item