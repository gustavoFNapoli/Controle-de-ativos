from database import db

class AtivoModel(db.Model):
    __tablename__ = 'ativos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    categoria = db.Column(db.Integer)
    responsavel = db.Column(db.String)
    setor = db.Column(db.String)
    localizacao = db.Column(db.String)