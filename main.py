from repository.ArquivoRepository import ArquivoRepository
from repository.Repositorio import Repository
from utils.Menu import Menu

if __name__ == '__main__':

    opcao = input("Digite A para arquivo ou B para banco de dados: ")

    if opcao.lower() == "a":
        repo = ArquivoRepository()
    elif opcao.lower() == "b":
        repo = Repository()
    else:
        print("Valor invalido")
        exit()

    menu = Menu(repo)
    menu.inicial()