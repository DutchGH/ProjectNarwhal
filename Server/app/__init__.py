from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_material import Material


app = Flask(__name__)
app.config.from_object('config')
Material(app)
db = SQLAlchemy(app)

from app import views
