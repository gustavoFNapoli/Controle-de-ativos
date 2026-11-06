from repository.VulnerabilidadesAtivosRepository import VulnerabilidadesAtivosRepository
from utils.Ferramentas import Ferramentas


class VulnerabilidadesAtivosService:
    def __init__(self):
        self.repository = VulnerabilidadesAtivosRepository()

    def vincular(self, formulario):
        try:
            self.repository.vincular(formulario["id_ativo"], formulario["id_vulnerabilidade"])
            return Ferramentas.resultado(True, "Vinculo criado")
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao criar vinculo erro: {e}")

    def desvincular(self, formulario):
        try:
            self.repository.desvincular(formulario["id_ativo"], formulario["id_vulnerabilidade"])
            return Ferramentas.resultado(True, "Vinculo desfeito")
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao tirar vinculo erro: {e}")

    def listar_por_ativo(self, ativo_id):
        try:
            vulnerabilidades = self.repository.list_by_ativo(int(ativo_id))

            return Ferramentas.resultado(
                True,
                "Vulnerabilidades encontradas!",
                vulnerabilidades
            )

        except Exception as e:
            return Ferramentas.resultado(
                False,
                f"Erro ao buscar vulnerabilidades vinculadas: {e}"
            )