from app import db

class VulnerabilidadeModel(db.Model):
    __tablename__ = 'vulnerabilidades'
    id = db.Column(db.Integer, primary_key=True)