from Repositorio import Repository
from model.Ativos import Ativo
from model.enuns.Categorias import Categoria


class AtivosService:
    def __init__(self):
        self.repository = Repository()

    def exibir_lista_de_ativos(self):
        print(self.repository.find_all())

    def grava_ativo(self):
        self.repository.insert(self.receber_ativos())

    def receber_ativos(self):
        nome = input("Digite o nome do ativo: ")
        categoria = self.recebe_categoria()
        responsavel = input("Digite o nome do responsavel do ativo\nResponsavel: ")
        setor = input("Digite o nome do setor do ativo: ")
        localizacao = input("Digite o nome do localizacao do ativo: ")
        vulnerabilidades = self.recebe_vulnerabilidades()

        return Ativo(nome, categoria, responsavel, setor, localizacao, vulnerabilidades)

    def recebe_categoria(self):
        while True:
            try:
                categoria = int(input("Escolha a categoria que melhor se encaixa para o ativo!\ncategorias:\n"
                          "servidor = 1 \n"
                          "software licencidado = 2\n"
                          "banco_de_dados = 3\n"
                          "aplicacao = 4\n"
                          "equipamento = 5\n>> "))
            except ValueError:
                print("Digite um valor dentro das categorias listadas")
            else:
                if 0 < categoria <= 6:
                    return Categoria(categoria)
                else:
                    print("Categoria não encontrada tente novamente")

    def recebe_vulnerabilidades(self):
        while True:
            try:




    def find_by_id(self, id):
        return self.repository.find_by_id(id)

    def find_by_nome(self, nome):
        return self.repository.find_by_nome(nome)

    def atualizar(self, ativo:Ativo):
        self.repository.update(ativo)

    def update_vulnerabilidades(self, vulnerabilidades, id):
        self.update_vulnerabilidades(vulnerabilidades, id)