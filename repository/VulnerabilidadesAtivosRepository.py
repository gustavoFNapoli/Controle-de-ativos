from database import db
from model.AtivoFactory import AtivoFactory
from model.VulnerabilidadeFactory import VulnerabilidadeFactory
from model.Vulnerabilidades import Vulnerabilidade
from repository.models.AtivoModel import AtivoModel
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel
from repository.models.VulnerabilidadesAtivosModel import VulnerabilidadesAtivos


class VulnerabilidadesAtivosRepository:

    def vincular(self, ativo_id, vulnerabilidade_id):
        uni = VulnerabilidadesAtivos(
            id_ativo = ativo_id,
            id_vulnerabilidade = vulnerabilidade_id
        )
        db.session.add(uni)
        db.session.commit()

    def desvincular(self, ativo_id, vulnerabilidade_id):
        uni = db.session.execute(db.select(VulnerabilidadesAtivos).where(VulnerabilidadesAtivos.id_ativo == ativo_id, VulnerabilidadesAtivos.id_vulnerabilidade == vulnerabilidade_id)).scalar_one_or_none()

        if uni is None:
            return False

        db.session.delete(uni)
        db.session.commit()
        return True

    def list_by_ativo(self, ativo_id):
        uni = db.session.execute(db.select(VulnerabilidadeModel)
                                 .join(VulnerabilidadesAtivos,
                                       VulnerabilidadesAtivos.id_vulnerabilidade == VulnerabilidadeModel.id)
                                 .where(VulnerabilidadesAtivos.id_ativo == ativo_id)).scalars().all()

        if not uni:
            return []

        return [VulnerabilidadeFactory.from_vulnerabilidade_model(vulnerabilidade) for vulnerabilidade in uni]

    def list_by_vulnerabilidade(self, vulnerabilidade_id):
        uni = db.session.execute(db.select(AtivoModel)
                                 .join(VulnerabilidadesAtivos,
                                       VulnerabilidadesAtivos.id_ativo == AtivoModel.id)
                                 .where(VulnerabilidadesAtivos.id_vulnerabilidade == vulnerabilidade_id)).scalars().all()

        if not uni:
            return []

        return [AtivoFactory.from_ativo_model(ativo) for ativo in uni]