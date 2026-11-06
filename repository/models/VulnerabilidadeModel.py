from database import db

class VulnerabilidadeModel(db.Model):
    __tablename__ = 'vulnerabilidades'

    id = db.Column(db.Integer, primary_key=True)
    vulnerabilidade = db.Column(db.String(255))
    severidade = db.Column(db.Integer)
    cvss_score = db.Column(db.Float, nullable=False, default=0)
    tipo = db.Column(db.Integer)
    status = db.Column(db.Integer)