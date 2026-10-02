from database import db
from model.Vulnerabilidades import Vulnerabilidade
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel


class VulnerabilidadesRepository:

    def find_all(self):
        vulnerabilidades = db.session.execute(db.select(VulnerabilidadeModel)).scalars().all()
        return [Vulnerabilidade.fromVulnerabilidadeModel(vulnerabilidade) for vulnerabilidade in vulnerabilidades]

    def find_by_id(self, id):
        vulnerabilidade = db.session.get(VulnerabilidadeModel, id)

        if vulnerabilidade is None:
            return None
        return Vulnerabilidade.fromVulnerabilidadeModel(vulnerabilidade)

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
