from database import db

class AtivoModel(db.Model):
    __tablename__ = 'ativos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    categoria = db.Column(db.Integer)
    responsavel = db.Column(db.String(255))
    setor = db.Column(db.String(255))
    localizacao = db.Column(db.String(255))