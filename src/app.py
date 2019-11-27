from flask import Flask, url_for, render_template
import flask_login

import models

# Initializing Flask
app = Flask(__name__)

# Authentication
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#class User(flask_login.UserMixin):
#    pass

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/api/signup')
def signup_API():
    # user_temp = models.User(email="andra.antariksa@gmail.com", password="andra123")
    # models.session.add(user_temp)
    # models.session.commit()
    return "OK"

@app.route('/@<username>/<product_slug>')
def product(username, product_slug):
    return render_template("product.html")