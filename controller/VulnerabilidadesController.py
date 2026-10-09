from flask import Blueprint, render_template, request, redirect, url_for

from service.VulnerabilidadesService import VulnerabilidadesService


class VulnerabilidadesController:
    def __init__(self):
        self.service = VulnerabilidadesService()
        self.controller = Blueprint("vulnerabilidades", __name__)
        self.registrar_rotas()

    def registrar_rotas(self):

        @self.controller.route("/vulnerabilidades", methods=["GET"])
        def listar_vulnerabilidades():
            resultado = self.service.achar_todos()

            if not resultado["sucesso"]:
                return render_template(
                    "vulnerabilidades.html",
                    ativos=[],
                    erro=resultado["mensagem"]
                )
            return render_template(
                "vulnerabilidades.html",
                ativos=resultado["dados"],
                erro=None
            )

        @self.controller.route("/vulnerabilidades/novo", methods=["GET", "POST"])
        def nova_vulnerabilidade():
            if request.method == "POST":
                resultado = self.service.grava_vulnerabilidade(request.form)

                if resultado["sucesso"]:
                    return redirect(url_for("vulnerabilidades.listar_vulnerabilidades"))
                return render_template(
                    "nova_vulnerabilidade.html",
                    erro=resultado["mensagem"],
                    formulario=request.form
                )
            return render_template(
                "nova_vulnerabilidade.html",
                erro=None,
                formulario={}
            )

        @self.controller.route("/vulnerabilidades/editar/<int:id>", methods=["GET", "POST"])
        def editar_vulnerabilidade(id):

            if request.method == "POST":
                formulario = request.form.to_dict()
                formulario["id"] = id

                resultado = self.service.atualizar(formulario)

                if resultado["sucesso"]:
                    return redirect(url_for("vulnerabilidades.listar_vulnerabilidades"))

                ativo_resultado = self.service.buscar_por_id(id)

                if ativo_resultado["dados"] is None:
                    return redirect(url_for("vulnerabilidades.listar_vulnerabilidades"))

                return render_template(
                    "editar_vulnerabilidade.html",
                    ativo=ativo_resultado["dados"],
                    erro=resultado["mensagem"],
                    formulario=formulario
                )

            resultado = self.service.buscar_por_id(id)

            if not resultado["sucesso"] or resultado["dados"] is None:
                return redirect(url_for("vulnerabilidades.listar_vulnerabilidades"))

            return render_template(
                "editar_vulnerabilidade.html",
                ativo=resultado["dados"],
                erro=None,
                formulario=None
            )

    def get_controller(self):
        return self.controller