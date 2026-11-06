from database import db

class VulnerabilidadesAtivos(db.Model):
    __tablename__ = 'vulnerabilidades_ativos'
    id_ativo = db.Column(db.Integer, db.ForeignKey("ativos.id"), primary_key=True)
    id_vulnerabilidade = db.Column(db.Integer, db.ForeignKey("vulnerabilidades.id"), primary_key=True)