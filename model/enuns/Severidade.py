from enum import Enum

class Severidade(Enum):
    baixa = 1
    media = 2
    alta = 3
    critica = 4

    def get_by_number(numero):
        for item in Severidade:
            if item.value == numero:
                return item