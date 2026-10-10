from flask import Flask

from controller.AtivosController import AtivosController
from controller.MenuController import MenuController
from controller.VulnerabilidadesController import VulnerabilidadesController
from database import db

from repository.models.AtivoModel import AtivoModel
from repository.models.VulnerabilidadeModel import VulnerabilidadeModel
from repository.models.VulnerabilidadesAtivosModel import VulnerabilidadesAtivos

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gustavo:123456@localhost:3306/controle_ativos'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    menu_controller = MenuController()
    ativo_controller = AtivosController()
    vulnerabilidade_controller = VulnerabilidadesController()

    app.register_blueprint(menu_controller.get_controller())
    app.register_blueprint(ativo_controller.get_controller())
    app.register_blueprint(vulnerabilidade_controller.get_controller())

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)