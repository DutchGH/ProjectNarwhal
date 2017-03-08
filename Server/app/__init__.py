from flask import Flask
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from flask_login import LoginManager
=======

>>>>>>> frontend

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
<<<<<<< HEAD
login_manager = LoginManager()
login_manager.init_app(app)

from app import views
from app import models
=======

from app import views
>>>>>>> frontend
