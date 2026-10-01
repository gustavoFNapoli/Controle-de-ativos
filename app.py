from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from utils.Menu import Menu

app = Flask(__name__)

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)
    menu = Menu()
    menu.inicial()