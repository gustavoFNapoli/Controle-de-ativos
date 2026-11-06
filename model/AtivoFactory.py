from model.Aplicacao import Aplicacao
from model.Ativos import Ativo
from model.BancoDeDados import BancoDeDados
from model.Equipamento import Equipamento
from model.Servidor import Servidor
from model.Software import Software
from model.enuns.Categorias import Categoria
from repository.models.AtivoModel import AtivoModel


class AtivoFactory:

    @staticmethod
    def from_ativo_model(ativo:AtivoModel):

        categoria = Categoria.get_by_number(ativo.categoria)

        if categoria == Categoria.aplicacao:
            return Aplicacao(
                ativo.id,
                ativo.nome,
                ativo.responsavel,
                ativo.setor,
                ativo.localizacao
            )
        if categoria == Categoria.banco_de_dados:
            return BancoDeDados(
                ativo.id,
                ativo.nome,
                ativo.responsavel,
                ativo.setor,
                ativo.localizacao
            )
        if categoria == Categoria.equipamento:
            return Equipamento(
                ativo.id,
                ativo.nome,
                ativo.responsavel,
                ativo.setor,
                ativo.localizacao
            )
        if categoria == Categoria.servidor:
            return Servidor(
                ativo.id,
                ativo.nome,
                ativo.responsavel,
                ativo.setor,
                ativo.localizacao
            )
        if categoria == Categoria.software_licenciado:
            return Software(
                ativo.id,
                ativo.nome,
                ativo.responsavel,
                ativo.setor,
                ativo.localizacao
            )

        return Ativo(
            ativo.id,
            ativo.nome,
            ativo.categoria,
            ativo.responsavel,
            ativo.setor,
            ativo.localizacao
        )

    @staticmethod
    def gerar_ativo(nome, categoria, responsavel, setor, localizacao, id=None):

        categoria = Categoria.get_by_number(int(categoria))

        if categoria == Categoria.aplicacao:
            return Aplicacao(
                id,
                nome,
                responsavel,
                setor,
                localizacao
            )
        if categoria == Categoria.banco_de_dados:
            return BancoDeDados(
                id,
                nome,
                responsavel,
                setor,
                localizacao
            )
        if categoria == Categoria.equipamento:
            return Equipamento(
                id,
                nome,
                responsavel,
                setor,
                localizacao
            )
        if categoria == Categoria.servidor:
            return Servidor(
                id,
                nome,
                responsavel,
                setor,
                localizacao
            )
        if categoria == Categoria.software_licenciado:
            return Software(
                id,
                nome,
                responsavel,
                setor,
                localizacao
            )

        return None