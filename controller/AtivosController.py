from flask import Blueprint, render_template, request, redirect, url_for
from service.AtivosService import AtivosService


class AtivosController:
    def __init__(self):
        self.service = AtivosService()
        self.controller = Blueprint("ativos", __name__)
        self.registrar_rotas()

    def registrar_rotas(self):

        @self.controller.route("/ativos", methods=["GET"])
        def listar_ativos():
            resultado = self.service.achar_todos_com_vulnerabilidades()

            if not resultado["sucesso"]:
                return render_template(
                    "ativos.html",
                    ativos=[],
                    erro=resultado["mensagem"]
                )
            return render_template(
                "ativos.html",
                ativos=resultado["dados"],
                erro=None
            )

        @self.controller.route("/ativos/novo", methods=["GET", "POST"])
        def novo_ativo():
            if request.method == "POST":
                resultado = self.service.grava_ativo(request.form)

                if resultado["sucesso"]:
                    return redirect(url_for("ativos.listar_ativos"))
                return render_template(
                    "novo_ativo.html",
                    erro=resultado["mensagem"],
                    formulario=request.form
                )
            return render_template(
                "novo_ativo.html",
                erro=None,
                formulario={}
            )

    def get_controller(self):
        return self.controller