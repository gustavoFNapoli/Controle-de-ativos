from enum import Enum

class Status(Enum):
    resolvido = 1
    em_analise = 2
    aceito = 3

    def get_by_number(numero:int):
        for item in Status:
            if item.value == numero:
                return item