import json
from dataclasses import dataclass

from model.Vulnerabilidades import Vulnerabilidade
from model.enuns.Categorias import Categoria

@dataclass
class Ativo:
    def __init__(self, id, nome, categoria, responsavel, setor, localizacao, vulnerabilidades):
        self.id = id
        self.nome = nome
        self.categoria = Categoria.get_by_number(int(categoria))
        self.responsavel = responsavel
        self.setor = setor
        self.localizacao = localizacao
        if isinstance(vulnerabilidades, str):
            self.vulnerabilidades = json.loads(vulnerabilidades)
        else:
            self.vulnerabilidades = vulnerabilidades

    def __str__(self):
        return (f"Id: {self.id}, Nome: {self.nome}, "
                f"Categoria: {self.categoria.name}, Responsavel: {self.responsavel}, "
                f"Setor: {self.setor}, Localizaçao: {self.localizacao}"
                f"\n{self.listar_vulnerabilidades()}")


    def adicionar_vulnerabilidade(self, vulnerabilidade: Vulnerabilidade):
        self.vulnerabilidades['lista'].append(vulnerabilidade.to_json())

    def listar_vulnerabilidades(self):
        if len(self.vulnerabilidades["lista"]) == 0:
            return "Ativo sem vulnerabilidades conhecidas"
        else:
            texto = "Vulnerabilidades encontradas:\n"
            for vul in self.vulnerabilidades["lista"]:
                texto+=f"Nome/Host: {vul['vulnerabilidade']}, Severidade: {vul['severidade']}, Tipo: {vul['tipo']}, Status: {vul['status']}\n"
            return texto