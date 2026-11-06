from database import db


class DependenciaAtivoModel(db.Model):
    __tablename__ = "dependencias_ativos"
    __table_args__ = (
        db.CheckConstraint("id_ativo <> id_dependencia", name="ck_dependencia_sem_ciclo_direto"),
        db.CheckConstraint("fracao >= 0 AND fracao < 1", name="ck_dependencia_fracao"),
    )

    id_ativo = db.Column(db.Integer, db.ForeignKey("ativos.id"), primary_key=True)
    id_dependencia = db.Column(db.Integer, db.ForeignKey("ativos.id"), primary_key=True)
    fracao = db.Column(db.Float, nullable=False)
