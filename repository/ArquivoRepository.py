import json

from model.Ativos import Ativo
from repository.Repo import Repo


class ArquivoRepository(Repo):

    def __init__(self):
        self.arquivo = 'ativos.json'

    def ler(self):
        try:
            with open(self.arquivo, "r") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return []

    def escrever(self, dados):
        with open(self.arquivo, "w") as arquivo:
            json.dump(dados, arquivo)

    def insert(self, ativo: Ativo) -> None:
        dados = self.ler()
        if dados:
            ativo.id = max(item["id"] for item in dados) + 1
        else:
            ativo.id = 1
        dados.append({
            "id": ativo.id,
            "nome": ativo.nome,
            "categoria": ativo.categoria.value,
            "responsavel": ativo.responsavel,
            "setor": ativo.setor,
            "localizacao": ativo.localizacao,
            "vulnerabilidades": ativo.vulnerabilidades
        })
        self.escrever(dados)

    def find_all(self):
        dados = self.ler()
        return [Ativo(**item) for item in dados]

    def find_by_id(self, id):
        dados = self.ler()
        for item in dados:
            if id == item["id"]:
                return Ativo(**item)
        return None

    def find_by_nome(self, nome):
        dados = self.ler()
        lista = []
        for item in dados:
            if nome == item["nome"]:
                lista.append(Ativo(**item))
        return lista

    def update(self, ativo: Ativo) -> None:
        dados = self.ler()
        for item in dados:
            if ativo.id == item["id"]:
                item["nome"] = ativo.nome
                item["categoria"] = ativo.categoria.value
                item["responsavel"] = ativo.responsavel
                item["setor"] = ativo.setor
                item["localizacao"] = ativo.localizacao
                item["vulnerabilidades"] = json.dumps(ativo.vulnerabilidades, default=lambda obj: obj.value)
                break
        self.escrever(dados)

    def delete_ativo(self, id) -> None:
        dados = self.ler()
        for item in dados:
            if item["id"] == id:
                dados.remove(item)
                break
        self.escrever(dados)