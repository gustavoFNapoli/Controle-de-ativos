from app import db

class AtivosModel(db.Model):
    __tablename__ = 'ativos'
    id = db.Column(db.Integer, primary_key=True)
