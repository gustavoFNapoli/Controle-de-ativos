from model.AtivoFactory import AtivoFactory
from repository.AtivoRepository import AtivoRepository
from repository.VulnerabilidadesAtivosRepository import VulnerabilidadesAtivosRepository
from utils.Ferramentas import Ferramentas


class AtivosService:
    def __init__(self):
        self.repository = AtivoRepository()
        self.vulnerabilidade_repository = VulnerabilidadesAtivosRepository()

    def achar_todos(self):
        try:
            return Ferramentas.resultado(True, "Ativos encontrados!", self.repository.find_all())
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao encontrar ativos erro: {e}")

    def achar_todos_com_vulnerabilidades(self):
        try:
            ativos = self.repository.find_all()
            resultado = []

            for ativo in ativos:
                vulnerabilidades = self.vulnerabilidade_repository.list_by_ativo(ativo.getId())
                resultado.append({
                    "ativo": ativo,
                    "vulnerabilidades": vulnerabilidades
                })

            return Ferramentas.resultado(True, "Ativos encontrados!", resultado)
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao encontrar ativos erro: {e}")

    def buscar_por_id(self, id):
        try:
            ativo = self.repository.find_by_id(int(id))
            if not ativo:
                return Ferramentas.resultado(True, "Nenhum ativo encontrado com esse id")
            return Ferramentas.resultado(True, "Ativo encontrado", ativo)
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao procurar ativo erro :{e}")

    def buscar_por_nome(self, nome):
        try:
            ativos = self.repository.find_by_nome(nome)
            if not ativos:
                return Ferramentas.resultado(True, "Nenhum ativo encontrado com esse id")
            return Ferramentas.resultado(True, "Ativos encontrados", ativos)
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao procurar ativos erro :{e}")

    def deletar_ativo(self, id):
        try:
            deletado = self.repository.delete(int(id))
            if deletado:
                return Ferramentas.resultado(True, "Ativo removido com sucesso")
            else:
                return Ferramentas.resultado(False, "Nenhum ativo deletado")
        except Exception as e:
            return Ferramentas.resultado(False, f"Falha ao remover ativo erro: {e}")

    def grava_ativo(self, formulario):
        try:
            ativo = AtivoFactory.gerar_ativo(formulario.get("nome"),
                                             formulario.get("categoria"),
                                             formulario.get("responsavel"),
                                             formulario.get("setor"),
                                             formulario.get("localizacao"))
            if not ativo:
                return Ferramentas.resultado(False, "Categoria invalida para o ativo")
            self.repository.insert(ativo)
            return Ferramentas.resultado(True, "Ativo armazenado com sucesso")
        except Exception as e:
            return Ferramentas.resultado(False, f"Erro ao tentar gravar o ativo erro: {e}")


    def atualizar(self, formulario):
        try:
            ativo = AtivoFactory.gerar_ativo(formulario.get("nome"),
                                             formulario.get("categoria"),
                                             formulario.get("responsavel"),
                                             formulario.get("setor"),
                                             formulario.get("localizacao"),
                                             formulario.get("id"))
            if not ativo:
                return Ferramentas.resultado(False, "Categoria invalida para o ativo")
            atualizado = self.repository.update(ativo)
            if atualizado is None:
                return Ferramentas.resultado(False, "Não existe esse ativo para ser atualizado")
            return Ferramentas.resultado(True, "Ativo atualizado com sucesso", atualizado)
        except Exception as e:
            return Ferramentas.resultado(False, f"Erro ao tentar atualizar o ativo erro: {e}")
