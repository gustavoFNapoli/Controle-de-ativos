class Ferramentas:

    @staticmethod
    def resultado(sucesso, mensagem, dados=None):
        return {
            "sucesso": sucesso,
            "mensagem": mensagem,
            "dados": dados
        }