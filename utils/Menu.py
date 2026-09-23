from service.AtivosService import AtivosService


class Menu:
    def __init__(self):
        self.service = AtivosService()

    def inicial(self):
        print('Bem vindo ao Controle de ativos 1.0')
        mensagem_despedida = 'Obrigado por usar nossos serviços, ate a proxima!!'
        while True:
            try:
                opcao = int(input('O que deseja fazer?\nEscolha a função que melhor lhe ajudar\n'
                                  '1 - Exibir lista de Ativos\n'
                                  '2 - Buscar por Nome\n'
                                  '3 - Buscar por Id\n'
                                  '4 - Adicionar ativo\n'
                                  '5 - Atualizar ativo\n'
                                  '6 - Remover ativo\n'
                                  '7 - Sair\n>> '))
            except ValueError:
                print('Por valor digite um valor entre 1, 2 ou 3')
            else:
                if opcao == 1:
                    self.service.achar_todos()
                elif opcao == 2:
                    self.service.buscar_por_nome()
                elif opcao == 3:
                    self.service.buscar_por_id()
                elif opcao == 4:
                    self.service.grava_ativo()
                elif opcao == 5:
                   self.menu_atualizacao()
                elif opcao == 6:
                    self.service.deletar_ativo()
                elif opcao == 7:
                    print(mensagem_despedida)
                    break
                else:
                    print('Opção invalida tente novamente')

    def menu_atualizacao(self):
        try:
            identificador = int(input("Digite o Id do ativo a ser buscado: "))
            ativo = self.service.find_by_id(identificador)
            if not ativo:
                print("Nenhum ativo encontrado com esse id")
                return
        except ValueError:
            print("Valor invalido tente novamente")
        else:
            print("Ativo encontrado:")
            print("----------------------------||----------------------------")
            print(ativo)
            print("----------------------------||----------------------------")
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
                    ativo.categoria = self.service.recebe_categoria()
                elif opcao == 3:
                    ativo.responsavel = input("Digite o nome do novo Responsavel do ativo: ")
                elif opcao == 4:
                    ativo.setor = input("Digite qual é o novo setor do ativo: ")
                elif opcao == 5:
                    ativo.localizacao = input("Digite qual é a nova localização do ativo: ")
                elif opcao == 6:
                    ativo.vulnerabilidades = self.service.recebe_vulnerabilidades(ativo.vulnerabilidades, "Adicionar vulnerabilidade?(s/n): ")
                elif opcao == 7:
                    ativo.vulnerabilidades = self.service.remover_vulnerabilidade(ativo.vulnerabilidades)
                else:
                    self.service.atualizar(ativo)
                    break