from enum import Enum

class Tipo(Enum):
    software = 1
    rede_infra = 2
    configuracao = 3

    def get_by_number(numero:int):
        for item in Tipo:
            if item.value == numero:
                return item