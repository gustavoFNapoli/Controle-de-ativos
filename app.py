from flask import Flask
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

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)