from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy

# Initializing flask
app = Flask(__name__)
app.secret_key = "Cikadev"

# Initializing database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:123@localhost:5432/bojonegoro"
db = SQLAlchemy(app)

# Initializing authentication
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

import src.handler