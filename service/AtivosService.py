import json

from repository.Repositorio import Repository
from model.Ativos import Ativo
from model.Vulnerabilidades import Vulnerabilidade
from model.enuns.Categorias import Categoria
from model.enuns.Severidade import Severidade
from model.enuns.Status import Status
from model.enuns.TiposVulnerabilidade import Tipo


class AtivosService:
    def __init__(self):
        self.repository = Repository()

    def achar_todos(self):
        ativos = self.repository.find_all()
        self.exibir_lista_de_ativos(ativos)

    def exibir_lista_de_ativos(self, ativos):
        print("Ativos encontrados:")
        print("----------------------------||----------------------------")
        for ativo in ativos:
            print(ativo)
            print("----------------------------||----------------------------")

    def grava_ativo(self):
        self.repository.insert(self.receber_ativos())

    def receber_ativos(self):
        nome = input("Digite o nome do ativo: ")
        categoria = self.recebe_categoria()
        responsavel = input("Digite o nome do responsavel do ativo\nResponsavel: ")
        setor = input("Digite o nome do setor do ativo: ")
        localizacao = input("Digite o nome do localizacao do ativo: ")
        vulnerabilidades = self.recebe_vulnerabilidades({"lista":[]}, "Deseja cadastrar uma ou mais vulnerabilidades?(S/N)")

        return Ativo(None, nome, categoria, responsavel, setor, localizacao, vulnerabilidades)

    def recebe_categoria(self):
        while True:
            try:
                categoria = int(input("Escolha a categoria que melhor se encaixa para o ativo!\ncategorias:\n"
                          "servidor = 1 \n"
                          "software licenciado = 2\n"
                          "banco_de_dados = 3\n"
                          "aplicacao = 4\n"
                          "equipamento = 5\n>> "))
            except ValueError:
                print("Digite um valor dentro das categorias listadas")
            else:
                if 0 < categoria < 6:
                    return categoria
                else:
                    print("Categoria não encontrada tente novamente")

    def recebe_vulnerabilidades(self, vulnerabilidades, texto):
        prosseguir = self.continuar(texto)
        if prosseguir:
            while True:
                nome = input("Digite o nome da vulnerabilidade: ")
                vulnerabilidades["lista"].append(Vulnerabilidade(nome, self.recebe_severidades(), self.tipo_vulnerabilidades(), self.receber_status()).to_json())
                aux = self.continuar("Deseja adicionar mais alguma vulnerabilidade?(s/n)")
                if not aux:
                    break
        return vulnerabilidades

    def recebe_severidades(self):
        while True:
            try:
                severidade = int(input("Escolha a severidade que melhor se encaixa para a vulnerabilidade!\nSeveridades:\n"
                                      "baixa = 1\n"
                                      "media = 2\n"
                                      "alta = 3\n"
                                      "critica = 4\n>> "))
            except ValueError:
                print("Digite um valor dentro das Severidades listadas")
            else:
                if 0 < severidade < 5:
                    return Severidade.get_by_number(severidade)
                else:
                    print("Severidade não encontrada tente novamente")

    def receber_status(self):
        while True:
            try:
                status = int(input("Escolha o status que se encontra a vulnerabilidade!\nStatus:\n"
                                      "resolvido = 1 \n"
                                      "em analise = 2\n"
                                      "aceito = 3\n>> "))
            except ValueError:
                print("Digite um valor dentro dos Status listados")
            else:
                if 0 < status < 4:
                    return Status.get_by_number(status)
                else:
                    print("Status não encontrada tente novamente")

    def tipo_vulnerabilidades(self):
        while True:
            try:
                status = int(input("Escolha o tipo de vulnerabilidade!\nTipos:\n"
                                      "software = 1 \n"
                                      "rede e infra = 2\n"
                                      "configuracao = 3\n>> "))
            except ValueError:
                print("Digite um valor dentro dos Tipos listados")
            else:
                if 0 < status < 4:
                    return Tipo.get_by_number(status)
                else:
                    print("Tipo não encontrada tente novamente")

    def deletar_ativo(self):
        try:
            id = int(input('Digite o Id fo ativo a ser deletado: '))
            self.repository.delete_ativo(id)
            print("Ativo removido com sucesso")
        except ValueError:
            print("o valor digitado deve ser um inteiro")
        except IndexError:
            print("O id digitado não conta na tabela de ativos")

    def continuar(self, texto):
        while True:
            prosseguir = input(texto)
            if prosseguir.lower() == "s":
                return True
            elif prosseguir.lower() == "n":
                return False
            else:
                print("Valor invalido tente novamente")

    def buscar_por_id(self):
        try:
            identificador = int(input("Digite o Id do ativo a ser buscado: "))
            ativo = self.find_by_id(identificador)
            if not ativo:
                print("Nenhum ativo encontrado com esse id")
                return
        except ValueError:
            print("Valor invalido tente novamente")
        else:
            ativo.categoria = Categoria.get_by_number(ativo.categoria)
            print("Ativo encontrado:")
            print("----------------------------||----------------------------")
            print(ativo)
            print("----------------------------||----------------------------")

    def find_by_id(self, id):
        return self.repository.find_by_id(id)

    def buscar_por_nome(self):
        try:
            identificador = input("Digite o Id do ativo a ser buscado: ")
            self.find_by_nome(identificador)
        except IndexError:
            print("Nenhum ativo encontrado com esse nome")

    def find_by_nome(self, nome):
        ativos = self.repository.find_by_nome(nome)
        self.exibir_lista_de_ativos(ativos)

    def atualizar(self, ativo:Ativo):
        self.repository.update(ativo)

    def remover_vulnerabilidade(self, vulnerabilidades):
        prosseguir = self.continuar("Remover Vulnerabilidade?(s/n): ")
        if prosseguir:
            try:
                vulnerabilidade = input("Digite qual vulnerabilidade deseja remover: ")
                for i in range(len(vulnerabilidades["lista"])):
                    if vulnerabilidades["lista"][i]["vulnerabilidade"]== vulnerabilidade:
                        del vulnerabilidades["lista"][i]
                        print("Vulnerabilidade removida com sucesso")
                        break
            except IndexError:
                print("Falha ao tentar remover vulnerabilidade")
        return vulnerabilidades