import json
from dataclasses import dataclass

from model.Vulnerabilidades import Vulnerabilidade
from model.enuns.Categorias import Categoria

@dataclass
class Ativo:
    def __init__(self, id, nome, categoria, responsavel, setor, localizacao, vulnerabilidades):
        self.__id = id
        self.__nome = nome
        self.__categoria = Categoria.get_by_number(int(categoria))
        self.__responsavel = responsavel
        self.__setor = setor
        self.__localizacao = localizacao
        if isinstance(vulnerabilidades, str):
            self.__vulnerabilidades = json.loads(vulnerabilidades)
        else:
            self.__vulnerabilidades = vulnerabilidades

    def __str__(self):
        return (f"Id: {self.__id}, Nome: {self.__nome}, "
                f"Categoria: {self.__categoria.name}, Responsavel: {self.__responsavel}, "
                f"Setor: {self.__setor}, Localizaçao: {self.__localizacao}"
                f"\n{self.listar_vulnerabilidades()}")


    def adicionar_vulnerabilidade(self, vulnerabilidade: Vulnerabilidade):
        self.__vulnerabilidades['lista'].append(vulnerabilidade.to_json())

    def listar_vulnerabilidades(self):
        if len(self.__vulnerabilidades["lista"]) == 0:
            return "Ativo sem vulnerabilidades conhecidas"
        else:
            texto = "Vulnerabilidades encontradas:\n"
            for vul in self.__vulnerabilidades["lista"]:
                texto+=f"Nome/Host: {vul['vulnerabilidade']}, Severidade: {vul['severidade']}, Tipo: {vul['tipo']}, Status: {vul['status']}\n"
            return texto

    def getId(self):
        return self.__id
    def setId(self, id):
        self.__id = id

    def getNome(self):
        return self.__nome
    def setNome(self, nome):
        self.__nome = nome

    def getCategoria(self):
        return self.__categoria
    def setCategoria(self, categoria):
        self.__categoria = Categoria.get_by_number(int(categoria))

    def getResponsavel(self):
        return self.__responsavel
    def setResponsavel(self, responsavel):
        self.__responsavel = responsavel

    def getSetor(self):
        return self.__setor
    def setSetor(self, setor):
        self.__setor = setor

    def getLocalizacao(self):
        return self.__localizacao
    def setLocalizacao(self, localizacao):
        self.__localizacao = localizacao

    def getVulnerabilidades(self):
        return self.__vulnerabilidades
    def setVulnerabilidades(self, vulnerabilidades):
        self.__vulnerabilidades = vulnerabilidades