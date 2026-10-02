from flask import Flask, render_template, request
from database import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)

    from repository.AtivoModel import AtivoModel
    from repository.VulnerabilidadeModel import VulnerabilidadeModel

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)