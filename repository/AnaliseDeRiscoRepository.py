from database import db
from repository.models.AtivoModel import AtivoModel
from repository.models.DependenciaAtivoModel import DependenciaAtivoModel
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel
from repository.models.VulnerabilidadesAtivosModel import VulnerabilidadesAtivos


class AnaliseDeRiscoRepository:
    def carregar_dados(self):
        ativos = db.session.execute(
            db.select(AtivoModel).order_by(AtivoModel.id)
        ).scalars().all()
        vulnerabilidades = db.session.execute(
            db.select(VulnerabilidadeModel).order_by(VulnerabilidadeModel.id)
        ).scalars().all()
        vinculos = db.session.execute(db.select(VulnerabilidadesAtivos)).scalars().all()
        dependencias = db.session.execute(
            db.select(DependenciaAtivoModel).order_by(
                DependenciaAtivoModel.id_ativo,
                DependenciaAtivoModel.id_dependencia,
            )
        ).scalars().all()

        return ativos, vulnerabilidades, vinculos, dependencias

    def salvar_dependencia(self, id_ativo, id_dependencia, fracao):
        if id_ativo == id_dependencia:
            return False, "Um ativo não pode depender de si mesmo."
        if not 0 <= fracao < 1:
            return False, "A fração deve ser maior ou igual a 0 e menor que 1."
        if (
            db.session.get(AtivoModel, id_ativo) is None
            or db.session.get(AtivoModel, id_dependencia) is None
        ):
            return False, "Selecione dois ativos cadastrados."

        existentes = db.session.execute(
            db.select(DependenciaAtivoModel).where(
                DependenciaAtivoModel.id_ativo == id_ativo
            )
        ).scalars().all()
        soma_das_fracoes = sum(
            dependencia.fracao
            for dependencia in existentes
            if dependencia.id_dependencia != id_dependencia
        )
        if soma_das_fracoes + fracao >= 1:
            return False, (
                "A soma das frações recebidas por um ativo deve ser menor que 1."
            )

        dependencia = db.session.get(
            DependenciaAtivoModel, (id_ativo, id_dependencia)
        )
        if dependencia is None:
            dependencia = DependenciaAtivoModel(
                id_ativo=id_ativo,
                id_dependencia=id_dependencia,
                fracao=fracao,
            )
            db.session.add(dependencia)
        else:
            dependencia.fracao = fracao
        db.session.commit()
        return True, "Dependência salva."

    def remover_dependencia(self, id_ativo, id_dependencia):
        dependencia = db.session.get(
            DependenciaAtivoModel, (id_ativo, id_dependencia)
        )
        if dependencia is None:
            return False
        db.session.delete(dependencia)
        db.session.commit()
        return True
