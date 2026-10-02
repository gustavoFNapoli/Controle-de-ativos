from model.Ativos import Ativo
from AtivoModel import AtivosModel, AtivoModel
from app import db

class AtivoRepository:

    def find_all(self):
        ativos = db.session.execute(db.select(AtivoModel)).scalars().all()
        return [Ativo.fromAtivoModel(ativo) for ativo in ativos]

    def find_by_id(self, id):
        ativo = db.session.get(AtivoModel, id)
        return Ativo.fromAtivoModel(ativo)

    def find_by_nome(self, nome):
        ativos = db.session.execute(db.session(AtivosModel).where(AtivosModel.nome == nome)).scalars().all()
        return [Ativo.fromAtivoModel(ativo) for ativo in ativos]

    def insert(self, ativo: Ativo):
        db.session.add(ativo.toAtivoModel())
        db.session.commit()

    def update(self, ativo: Ativo):
        model = db.session.get(AtivoModel, ativo.getId())

        if model is None:
            return None

        model.nome = ativo.nome
        model.categoria = ativo.categoria.value
        model.responsavel = ativo.responsavel
        model.setor = ativo.setor
        model.localizacao = ativo.localizacao

        db.session.commit()

        return ativo

    def delete(self, ativo: Ativo):
        model = db.session.get(AtivoModel, id)

        if model is None:
            return False

        db.session.delete(model)
        db.session.commit()

        return True
