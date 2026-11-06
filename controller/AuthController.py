from flask import Blueprint, redirect, render_template, request, session, url_for
from sqlalchemy import select
from werkzeug.security import check_password_hash

from database import db
from repository.models.UsuarioModel import UsuarioModel


class AuthController:
    def __init__(self):
        self.controller = Blueprint("auth", __name__)
        self.registrar_rotas()

    def registrar_rotas(self):
        @self.controller.route("/login", methods=["GET", "POST"])
        def login():
            erro = None
            if request.method == "POST":
                username = request.form.get("username", "").strip()
                password = request.form.get("password", "")
                usuario = db.session.execute(
                    select(UsuarioModel).where(UsuarioModel.username == username)
                ).scalar_one_or_none()

                if usuario is None or not check_password_hash(
                    usuario.password_hash, password
                ):
                    erro = "Usuário ou senha inválidos."
                else:
                    session.clear()
                    session["user_id"] = usuario.id
                    session["username"] = usuario.username
                    return redirect(url_for("menu.menu_inicial"))

            return render_template("login.html", erro=erro)

        @self.controller.route("/logout", methods=["POST"])
        def logout():
            session.clear()
            return redirect(url_for("auth.login"))

    def get_controller(self):
        return self.controller
