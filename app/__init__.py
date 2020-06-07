from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c4e928aed3d42753f492642344712767'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False

db 		= SQLAlchemy(app)
bcrypt 	= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'authorize'

from app import routes

