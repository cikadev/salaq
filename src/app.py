from flask import Flask, url_for, render_template
import flask_login

# Initializing Flask
app = Flask(__name__)

# Authentication
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, email):
        self.email = email
        self.password = password

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/@<username>/<product_slug>')
def product(username, product_slug):
    return f"{username}, {product_slug}"