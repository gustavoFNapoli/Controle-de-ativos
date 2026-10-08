from database import db

class VulnerabilidadeModel(db.Model):
    __tablename__ = 'vulnerabilidades'

    id = db.Column(db.Integer, primary_key=True)
    vulnerabilidade = db.Column(db.String(255))
    severidade = db.Column(db.Integer)
    tipo = db.Column(db.Integer)
    status = db.Column(db.Integer)