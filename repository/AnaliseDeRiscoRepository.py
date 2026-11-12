from database import db
from model.AtivoFactory import AtivoFactory
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
        ativos_por_id = {
            ativo.id: AtivoFactory.from_ativo_model(ativo) for ativo in ativos
        }
        dependencias_atualizadas = False
        for dependencia in dependencias:
            ativo_dependente = ativos_por_id.get(dependencia.id_ativo)
            if ativo_dependente is None:
                continue
            fator_transmissao = ativo_dependente.getFatorTransmissaoRisco()
            if dependencia.fracao != fator_transmissao:
                dependencia.fracao = fator_transmissao
                dependencias_atualizadas = True
        if dependencias_atualizadas:
            db.session.commit()

        return ativos, vulnerabilidades, vinculos, dependencias

    def salvar_dependencia(self, id_ativo, id_dependencia):
        if id_ativo == id_dependencia:
            return False, "Um ativo não pode depender de si mesmo."
        ativo = db.session.get(AtivoModel, id_ativo)
        if ativo is None or db.session.get(AtivoModel, id_dependencia) is None:
            return False, "Selecione dois ativos cadastrados."
        fracao = AtivoFactory.from_ativo_model(ativo).getFatorTransmissaoRisco()
        if not 0 <= fracao < 1:
            return False, "O tipo do ativo não possui um fator de transmissão válido."

        existentes = db.session.execute(
            db.select(DependenciaAtivoModel).where(
                DependenciaAtivoModel.id_ativo == id_ativo
            )
        ).scalars().all()
        quantidade_outras_dependencias = sum(
            dependencia.id_dependencia != id_dependencia
            for dependencia in existentes
        )
        soma_das_fracoes = quantidade_outras_dependencias * fracao
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
