from repository.VulnerabilidadesAtivosRepository import VulnerabilidadesAtivosRepository
from utils.Ferramentas import Ferramentas


class VulnerabilidadesAtivosService:
    def __init__(self):
        self.repository = VulnerabilidadesAtivosRepository()

    def vincular(self, formulario):
        try:
            self.repository.vincular(formulario["ativo_id"], formulario["vulnerabilidade_id"])
            return Ferramentas.resultado(True, "Vinculo criado")
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao criar vinculo erro: {e}")

    def desvincular(self, formulario):
        try:
            self.repository.desvincular(formulario["ativo_id"], formulario["vulnerabilidade_id"])
            return Ferramentas.resultado(True, "Vinculo desfeito")
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao tirar vinculo erro: {e}")
