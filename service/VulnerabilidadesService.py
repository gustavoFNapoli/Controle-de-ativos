from model.VulnerabilidadeFactory import VulnerabilidadeFactory
from repository.VulnerabilidadesRepository import VulnerabilidadesRepository
from utils.Ferramentas import Ferramentas


class VulnerabilidadesService:
    def __init__(self):
        self.repository = VulnerabilidadesRepository()

    def achar_todos(self):
        try:
            return Ferramentas.resultado(True, "Vulnerabilidades encontradas!", self.repository.find_all())
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao encontrar vulnerabilidades erro: {e}")

    def buscar_por_id(self, id):
        try:
            vulnerabilidade = self.repository.find_by_id(int(id))
            if not vulnerabilidade:
                return Ferramentas.resultado(True, "Nenhuma vulnerabilidade encontrada com esse id")
            return Ferramentas.resultado(True, "Vulnerabilidade encontrada", vulnerabilidade)
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao procurar vulnerabilidade erro :{e}")

    def buscar_por_nome(self, nome):
        try:
            vulnerabilidades = self.repository.find_by_nome(nome)
            if not vulnerabilidades:
                return Ferramentas.resultado(True, "Nenhuma vulnerabilidade encontrada com esse id")
            return Ferramentas.resultado(True, "Vulnerabilidades encontradas", vulnerabilidades)
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao procurar vulnerabilidade erro :{e}")

    def deletar_ativo(self, id):
        try:
            deletado = self.repository.delete(int(id))
            if deletado:
                return Ferramentas.resultado(True, "Vulnerabilidade removida com sucesso")
            return Ferramentas.resultado(False, "Não foi possivel remover vulnerabilidade")
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao remover vulnerabilidade erro: {e}")

    def grava_ativo(self, formulario):
        try:
            vulnerabilidade = VulnerabilidadeFactory.gerar_vulnerabilidade(formulario.get("vulnerabilidade"),
                                                                 formulario.get("severidade"),
                                                                 formulario.get("tipo"),
                                                                 formulario.get("status"))
            if not vulnerabilidade:
                return Ferramentas.resultado(False, "Falha ao gerar vulnerabilidade")
            self.repository.insert(vulnerabilidade)
            return Ferramentas.resultado(True, "Vulnerabilidade armazenada com sucesso")
        except Exception as e:
            return Ferramentas.resultado(False, f"Erro ao tentar gravar o vulnerabilidade erro: {e}")

    def atualizar(self, formulario):
        try:
            vulnerabilidade = VulnerabilidadeFactory.gerar_vulnerabilidade(formulario.get("vulnerabilidade"),
                                                                           formulario.get("severidade"),
                                                                           formulario.get("tipo"),
                                                                           formulario.get("status"))
            if not vulnerabilidade:
                return Ferramentas.resultado(False, "Falha ao gerar vulnerabilidade")
            atualizado = self.repository.update(vulnerabilidade)
            if atualizado is None:
                return Ferramentas.resultado(False, "Não existe essa vulnerabilidade para ser atualizada")
            return Ferramentas.resultado(True, "Vulnerabilidade atualizada com sucesso", atualizado)
        except Exception as e:
            return Ferramentas.resultado(False, f"Erro ao tentar atualizar a vulnerabilidade erro: {e}")