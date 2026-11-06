from flask import Blueprint, redirect, render_template, request, url_for

from service.AnaliseDeRiscoService import AnaliseDeRiscoService


class RiscoController:
    def __init__(self):
        self.service = AnaliseDeRiscoService()
        self.controller = Blueprint("riscos", __name__)
        self.registrar_rotas()

    def registrar_rotas(self):
        @self.controller.route("/riscos")
        def consultar_riscos():
            return self._renderizar()

        @self.controller.route("/riscos/dependencias", methods=["POST"])
        def salvar_dependencia():
            resultado = self.service.salvar_dependencia(request.form)
            if resultado["sucesso"]:
                return redirect(url_for("riscos.consultar_riscos"))
            return self._renderizar(erro=resultado["mensagem"])

        @self.controller.route("/riscos/dependencias/remover", methods=["POST"])
        def remover_dependencia():
            resultado = self.service.remover_dependencia(request.form)
            if resultado["sucesso"]:
                return redirect(url_for("riscos.consultar_riscos"))
            return self._renderizar(erro=resultado["mensagem"])

    def _renderizar(self, erro=None):
        resultado = self.service.calcular()
        dados = resultado["dados"] or {}
        return render_template(
            "riscos.html",
            ativos=dados.get("ativos", []),
            riscos=dados.get("riscos", []),
            dependencias=dados.get("dependencias", []),
            numero_condicao=dados.get("numero_condicao"),
            erro=erro or (None if resultado["sucesso"] else resultado["mensagem"]),
        )

    def get_controller(self):
        return self.controller
