from database import db
from model.VulnerabilidadeFactory import VulnerabilidadeFactory
from model.Vulnerabilidades import Vulnerabilidade
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel


class VulnerabilidadesRepository:

    def find_all(self):
        vulnerabilidades = db.session.execute(db.select(VulnerabilidadeModel)).scalars().all()
        return [VulnerabilidadeFactory.from_vulnerabilidade_model(vulnerabilidade) for vulnerabilidade in vulnerabilidades]

    def find_by_id(self, id):
        vulnerabilidade = db.session.get(VulnerabilidadeModel, id)

        if vulnerabilidade is None:
            return None
        return VulnerabilidadeFactory.from_vulnerabilidade_model(vulnerabilidade)

    def find_by_nome(self, nome):
        vulnerabilidades = db.session.execute(db.select(VulnerabilidadeModel).where(VulnerabilidadeModel.nome == nome)).scalars().all()
        return [VulnerabilidadeFactory.from_vulnerabilidade_model(vulnerabilidade) for vulnerabilidade in vulnerabilidades]

    def insert(self, vulnerabilidade:Vulnerabilidade):
        db.session.add(vulnerabilidade.toVulnerabilidadeModel())
        db.session.commit()

    def update(self, vulnerabilidade:Vulnerabilidade):
        vul = db.session.get(VulnerabilidadeModel, vulnerabilidade.getId())

        if vul is None:
            return None

        vul.vulnerabilidade = vulnerabilidade.getVulnerabilidade()
        vul.severidade = vulnerabilidade.getSeveridade().value
        vul.tipo = vulnerabilidade.getTipo().value
        vul.status = vulnerabilidade.getStatus().value

        db.session.commit()
        return vulnerabilidade

    def delete(self, id):
        vul = db.session.get(VulnerabilidadeModel, id)

        if vul is None:
            return False

        db.session.delete(vul)
        db.session.commit()
        return True
