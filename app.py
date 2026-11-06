import os
import secrets
from urllib.parse import quote_plus

import click
from flask import Flask, g, redirect, request, session, url_for
from sqlalchemy import inspect, text
from werkzeug.security import generate_password_hash

from controller.AtivosController import AtivosController
from controller.AuthController import AuthController
from controller.MenuController import MenuController
from controller.RiscoController import RiscoController
from controller.VulnerabilidadesController import VulnerabilidadesController
from controller.VulnerabilidadesAtivosController import VulnerabilidadesAtivosController
from database import db
from repository.models.AtivoModel import AtivoModel
from repository.models.DependenciaAtivoModel import DependenciaAtivoModel
from repository.models.UsuarioModel import UsuarioModel
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel
from repository.models.VulnerabilidadesAtivosModel import VulnerabilidadesAtivos


def create_app(test_config=None):
    app = Flask(__name__)
    database_uri = os.environ.get("DATABASE_URL")
    if not database_uri and os.environ.get("DB_HOST"):
        database_user = quote_plus(os.environ.get("DB_USER", ""))
        database_password = quote_plus(os.environ.get("DB_PASSWORD", ""))
        database_name = quote_plus(os.environ.get("DB_NAME", "controle_ativos"))
        database_uri = (
            f"mysql+pymysql://{database_user}:{database_password}"
            f"@{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '3306')}/{database_name}"
        )

    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        SQLALCHEMY_DATABASE_URI=database_uri or "sqlite:///controle_ativos.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "").lower() == "true",
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        columns = {
            column["name"]
            for column in inspect(db.engine).get_columns("vulnerabilidades")
        }
        if "cvss_score" not in columns:
            with db.engine.begin() as connection:
                connection.execute(text(
                    "ALTER TABLE vulnerabilidades "
                    "ADD COLUMN cvss_score FLOAT NOT NULL DEFAULT 0"
                ))

    controllers = (
        AuthController(),
        MenuController(),
        AtivosController(),
        VulnerabilidadesController(),
        VulnerabilidadesAtivosController(),
        RiscoController(),
    )
    for controller in controllers:
        app.register_blueprint(controller.get_controller())

    @app.before_request
    def require_login():
        if (
            request.endpoint is None
            or request.endpoint.startswith("auth.")
            or request.endpoint == "static"
        ):
            return None

        user_id = session.get("user_id")
        user = db.session.get(UsuarioModel, user_id) if user_id else None
        if user is None:
            session.clear()
            return redirect(url_for("auth.login"))

        g.current_user = user
        return None

    @app.context_processor
    def inject_authenticated_user():
        return {"authenticated_username": session.get("username")}

    @app.cli.command("create-admin")
    def create_admin():
        """Create a login account interactively."""
        username = click.prompt("Usuário").strip()
        if not username:
            raise click.ClickException("O usuário não pode ficar vazio.")
        if len(username) > 80:
            raise click.ClickException("O usuário deve ter no máximo 80 caracteres.")
        if db.session.execute(
            db.select(UsuarioModel).where(UsuarioModel.username == username)
        ).scalar_one_or_none():
            raise click.ClickException("Esse usuário já existe.")

        password = click.prompt(
            "Senha (mínimo de 12 caracteres)",
            hide_input=True,
            confirmation_prompt=True,
        )
        if len(password) < 12:
            raise click.ClickException("A senha deve ter pelo menos 12 caracteres.")

        db.session.add(UsuarioModel(
            username=username,
            password_hash=generate_password_hash(password),
        ))
        db.session.commit()
        click.echo("Usuário criado com sucesso.")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
