from model.AtivoFactory import AtivoFactory
from model.Ativos import Ativo
from repository.models.AtivoModel import AtivoModel
from database import db

class AtivoRepository:

    def find_all(self):
        ativos = db.session.execute(db.select(AtivoModel)).scalars().all()
        return [AtivoFactory.from_ativo_model(ativo) for ativo in ativos]

    def find_by_id(self, id):
        ativo = db.session.get(AtivoModel, id)

        if ativo is None:
            return None
        return AtivoFactory.from_ativo_model(ativo)

    def find_by_nome(self, nome):
        ativos = db.session.execute(db.select(AtivoModel).where(AtivoModel.nome == nome)).scalars().all()
        return [AtivoFactory.from_ativo_model(ativo) for ativo in ativos]

    def insert(self, ativo: Ativo):
        db.session.add(ativo.toAtivoModel())
        db.session.commit()

    def update(self, ativo: Ativo):
        model = db.session.get(AtivoModel, ativo.getId())

        if model is None:
            return None

        model.nome = ativo.getNome()
        model.categoria = ativo.getCategoria().value
        model.responsavel = ativo.getResponsavel()
        model.setor = ativo.getSetor()
        model.localizacao = ativo.getLocalizacao()

        db.session.commit()
        return ativo

    def delete(self, id):
        model = db.session.get(AtivoModel, id)

        if model is None:
            return False

        db.session.delete(model)
        db.session.commit()
        return True
