from enum import Enum

class Tipo(Enum):
    def get_by_number(numero):
        for item in Tipo:
            if item.value == numero:
                return item