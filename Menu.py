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
                                  '2 - Adicionar ativo\n'
                                  '3 - Remover ativo\n'
                                  '4 - Sair\n>> '))

                if opcao == 1:
                    self.service.exibir_lista_de_ativos()
                elif opcao == 2:
                    adicionar()
                elif opcao == 3:
                    remover()
                elif opcao == 4:
                    print(mensagem_despedida)
                    break
                else:
                    print('Opção invalida tente novamente')

            except ValueError:
                print('Por valor digite um valor entre 1, 2 ou 3')