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
            print("Id: {}, Nome: {}, Categoria: {}, Responsavel: {}, Setor: {}, Localizaçao: {}"
                  .format(ativo.id, ativo.nome, ativo.categoria, ativo.responsavel, ativo.setor, ativo.localizacao))
            ativo.vulnerabilidades = json.loads(ativo.vulnerabilidades)
            self.listar_vulnerabilidades(ativo.vulnerabilidades)

    def listar_vulnerabilidades(self, vulnerabilidades):
        if len(vulnerabilidades["lista"]) == 0:
            print("Ativo sem vulnerabilidades conhecidas")
        else:
            print("Vulnerabilidades encontradas:")
            for vul in vulnerabilidades["lista"]:
                print("Nome/Host: {}, Severidade: {}, Tipo: {}, Status: {}"
                      .format(vul["vulnerabilidade"], vul["severidade"], vul["tipo"], vul["status"]))
        print()
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
                    return Categoria.get_by_number(categoria)
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
            print("Ativo encontrado:")
            print("----------------------------||----------------------------")
            print("Id: {}, Nome: {}, Categoria: {}, Responsavel: {}, Setor: {}, Localizaçao: {}"
                  .format(ativo.id, ativo.nome, ativo.categoria, ativo.responsavel, ativo.setor, ativo.localizacao))
            ativo.vulnerabilidades = json.loads(ativo.vulnerabilidades)
            self.listar_vulnerabilidades(ativo.vulnerabilidades)


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

    def atualizar_ativo(self):
        try:
            identificador = int(input("Digite o Id do ativo a ser buscado: "))
            ativo = self.find_by_id(identificador)
            if not ativo:
                print("Nenhum ativo encontrado com esse id")
                return
        except ValueError:
            print("Valor invalido tente novamente")
        else:
            print("Ativo encontrado:")
            print("----------------------------||----------------------------")
            print("Id: {}, Nome: {}, Categoria: {}, Responsavel: {}, Setor: {}, Localizaçao: {}"
                  .format(ativo.id, ativo.nome, ativo.categoria, ativo.responsavel, ativo.setor, ativo.localizacao))
            ativo.categoria = Categoria(ativo.categoria)
            ativo.vulnerabilidades = json.loads(ativo.vulnerabilidades)
            self.listar_vulnerabilidades(ativo.vulnerabilidades)
            while True:
                opcao = int(input('O que deseja fazer?\nEscolha a função que melhor lhe ajudar\n'
                                    '1 - Atualizar Nome\n'
                                    '2 - Categoria\n'
                                    '3 - Responsavel\n'
                                    '4 - Setor\n'
                                    '5 - Localizaçao\n'
                                    '6 - adicionar vulnerabilidade\n'
                                    '7 - remover vulnerabilidade\n'
                                    '8 - Sair\n>> '))
                if opcao == 1:
                    ativo.nome = input("Digite o novo nome do ativo: ")
                elif opcao == 2:
                    ativo.categoria = self.recebe_categoria()
                elif opcao == 3:
                    ativo.responsavel = input("Digite o nome do novo Responsavel do ativo: ")
                elif opcao == 4:
                    ativo.setor = input("Digite qual é o novo setor do ativo: ")
                elif opcao == 5:
                    ativo.localizacao = input("Digite qual é a nova localização do ativo: ")
                elif opcao == 6:
                    ativo.vulnerabilidades = self.recebe_vulnerabilidades(ativo.vulnerabilidades, "Adicionar vulnerabilidade?(s/n): ")
                elif opcao == 7:
                    ativo.vulnerabilidades = self.remover_vulnerabilidade(ativo.vulnerabilidades)
                else:
                    self.atualizar(ativo)
                    break



    def remover_vulnerabilidade(self, vulnerabilidades):
        prosseguir = self.continuar("Remover Vulnerabilidade?(s/n): ")
        if prosseguir:
            try:
                vulnerabilidade = input("Digite qual vulnerabilidade deseja remover: ")
                for i in range(len(vulnerabilidades["lista"])):
                    if vulnerabilidades["lista"][i]["vulnerabilidade"]== vulnerabilidade:
                        del vulnerabilidades["lista"][i]
                        break
            except IndexError:
                print("Falha ao tentar remover vulnerabilidade")
        return vulnerabilidades