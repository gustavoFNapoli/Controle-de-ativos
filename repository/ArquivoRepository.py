import json
from json import JSONDecodeError

from model.Ativos import Ativo
from model.enuns.Categorias import Categoria
from repository.Repo import Repo


class ArquivoRepository(Repo):

    def __init__(self):
        self.arquivo = 'ativos.json'

    def ler(self):
        try:
            with open(self.arquivo, "r") as arquivo:
                return json.load(arquivo)
        except (FileNotFoundError, JSONDecodeError):
            return {}

    def escrever(self, dados):
        with open(self.arquivo, "w") as arquivo:
            json.dump(dados, arquivo)

    def insert(self, ativo: Ativo) -> None:
        dados = self.ler()
        if dados:
            ativo.id = max(map(int, dados.keys())) + 1
        else:
            ativo.id = 1

        dados[str(ativo.id)] = {
            "nome": ativo.nome,
            "categoria": ativo.categoria.value,
            "responsavel": ativo.responsavel,
            "setor": ativo.setor,
            "localizacao": ativo.localizacao,
            "vulnerabilidades": ativo.vulnerabilidades
        }
        self.escrever(dados)

    def find_all(self):
        dados = self.ler()
        ativos = []
        for id, item in dados.items():
            item['id']= int(id)
            ativos.append(Ativo(**item))
        return ativos

    def find_by_id(self, id):
        dados = self.ler()
        item = dados.get(str(id))
        if item is None:
            return None
        item["id"] = id
        return Ativo(**item)

    def find_by_nome(self, nome):
        dados = self.ler()
        ativos = []
        for id, item in dados.items():
            if nome.lower() == item["nome"].lower():
                item['id'] = int(id)
                ativos.append(Ativo(**item))
        return ativos

    def update(self, ativo: Ativo) -> None:
        dados = self.ler()
        id = str(ativo.id)
        dados[id] = {
            "nome": ativo.nome,
            "categoria": ativo.categoria.value,
            "responsavel": ativo.responsavel,
            "setor": ativo.setor,
            "localizacao": ativo.localizacao,
            "vulnerabilidades": ativo.vulnerabilidades
        }
        self.escrever(dados)

    def delete_ativo(self, id) -> None:
        dados = self.ler()
        dados.pop(str(id), None)
        self.escrever(dados)