from enum import Enum
import math

class Severidade(Enum):
    baixa = 1
    media = 2
    alta = 3
    critica = 4

    def get_by_number(numero:int):
        for item in Severidade:
            if item.value == numero:
                return item

    @staticmethod
    def get_by_cvss_score(nota: float):
        nota = float(nota)
        if not math.isfinite(nota) or not 0 <= nota <= 10:
            return None
        if nota < 3:
            return Severidade.baixa
        if nota < 6:
            return Severidade.media
        if nota < 9:
            return Severidade.alta
        return Severidade.critica