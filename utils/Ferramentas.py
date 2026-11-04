from cryptography.fernet import Fernet

class Ferramentas:

    @staticmethod
    def resultado(sucesso, mensagem, dados=None):
        return {
            "sucesso": sucesso,
            "mensagem": mensagem,
            "dados": dados
        }

    # 1. Gerar uma chave e salvá-la (em um caso real, guarde essa chave em segurança)
    chave = Fernet.generate_key()
    f = Fernet(chave)

    print(chave)

    # 2. Mensagem original (deve estar em bytes)
    mensagem = b"Texto super secreto em Python!"

    # 3. Criptografar a mensagem
    token = f.encrypt(mensagem)
    print("Mensagem criptografada:", token)

    # 4. Descriptografar a mensagem
    mensagem_original = f.decrypt(token)
    print("Mensagem descriptografada:", mensagem_original.decode())