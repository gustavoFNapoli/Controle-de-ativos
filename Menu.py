from AtivosService import AtivosService


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
                                  '5 - Atualizar vulnerabilidades de ativo\n'
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
                   break
                elif opcao == 6:
                    self.service.deletar_ativo()
                elif opcao == 7:
                    print(mensagem_despedida)
                    break
                else:
                    print('Opção invalida tente novamente')