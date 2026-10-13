from flask import Blueprint, render_template, request, redirect, url_for

from service.AtivosService import AtivosService
from service.VulnerabilidadesService import VulnerabilidadesService
from service.VulnerabilidadesAtivosService import VulnerabilidadesAtivosService


class VulnerabilidadesAtivosController:

    def __init__(self):
        self.ativos_service = AtivosService()
        self.vulnerabilidades_service = VulnerabilidadesService()
        self.vinculos_service = VulnerabilidadesAtivosService()

        self.controller = Blueprint("vinculos", __name__)

        self.registrar_rotas()

    def registrar_rotas(self):

        @self.controller.route("/vinculos", methods=["GET", "POST"])
        def gerenciar_vinculos():

            if request.method == "POST":

                formulario = request.form.to_dict()

                resultado = self.vinculos_service.vincular(formulario)

                if resultado["sucesso"]:
                    return redirect(
                        url_for(
                            "vinculos.gerenciar_vinculos",
                            ativo_id=formulario.get("id_ativo")
                        )
                    )

                erro = resultado["mensagem"]

            else:
                erro = None

            ativos_resultado = self.ativos_service.achar_todos()
            vulnerabilidades_resultado = self.vulnerabilidades_service.achar_todos()

            if not ativos_resultado["sucesso"]:
                return render_template(
                    "vinculos.html",
                    ativos=[],
                    vulnerabilidades=[],
                    vinculadas=[],
                    ativo_selecionado=None,
                    erro=ativos_resultado["mensagem"]
                )

            if not vulnerabilidades_resultado["sucesso"]:
                return render_template(
                    "vinculos.html",
                    ativos=ativos_resultado["dados"],
                    vulnerabilidades=[],
                    vinculadas=[],
                    ativo_selecionado=None,
                    erro=vulnerabilidades_resultado["mensagem"]
                )

            ativos = ativos_resultado["dados"]
            vulnerabilidades = vulnerabilidades_resultado["dados"]

            ativo_id = request.args.get("ativo_id")

            vinculadas = []
            ativo_selecionado = None

            if ativo_id:
                ativo_selecionado = next(
                    (
                        ativo for ativo in ativos
                        if ativo.getId() == int(ativo_id)
                    ),
                    None
                )

                if ativo_selecionado:
                    resultado_vinculadas = (
                        self.vinculos_service.listar_por_ativo(ativo_id)
                    )

                    if resultado_vinculadas["sucesso"]:
                        vinculadas = resultado_vinculadas["dados"]
                    else:
                        erro = resultado_vinculadas["mensagem"]

            return render_template(
                "vinculos.html",
                ativos=ativos,
                vulnerabilidades=vulnerabilidades,
                vinculadas=vinculadas,
                ativo_selecionado=ativo_selecionado,
                erro=erro
            )

        @self.controller.route("/vinculos/remover", methods=["POST"])
        def remover_vinculo():

            formulario = request.form.to_dict()

            resultado = self.vinculos_service.desvincular(formulario)

            if not resultado["sucesso"]:
                # Retorna à página do ativo e exibe a mensagem de erro.
                return redirect(
                    url_for(
                        "vinculos.gerenciar_vinculos",
                        ativo_id=formulario.get("id_ativo"),
                        erro=resultado["mensagem"]
                    )
                )

            return redirect(
                url_for(
                    "vinculos.gerenciar_vinculos",
                    ativo_id=formulario.get("id_ativo")
                )
            )

    def get_controller(self):
        return self.controller