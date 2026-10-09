from flask import Blueprint, render_template


class MenuController:

    def __init__(self):
        self.controller = Blueprint("menu", __name__)
        self.registrar_rotas()

    def registrar_rotas(self):

        @self.controller.route("/")
        def menu_inicial():
            return render_template("menu.html")

    def get_controller(self):
        return self.controller