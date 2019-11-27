from flask import Flask, render_template, request, flash, url_for, redirect
import flask_login
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import json

# Initializing Flask
app = Flask(__name__)
app.secret_key = "Cikadev"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:123@localhost:5432/bojonegoro"
db = SQLAlchemy(app)


class Users(flask_login.UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    name = db.Column(db.String)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return self.email

    @staticmethod
    def where_email(email):
        return Users.query.filter_by(email=email).first()

    @staticmethod
    def where_email_password(email, password):
        return Users.query.filter_by(email=email, password=password).first()


# Authentication
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    if email is not None:
        return Users.where_email(email)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for("signin"))


@app.route('/')
def home():
    return render_template("home.html", title="Home")

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for("signin"))

@app.route('/signin')
def signin():
    return render_template("signin.html", title="Signin")

@app.route("/api/signin", methods=["POST"])
def signin_API():
    email = request.form['email']
    password = request.form['password']

    signin_user = Users.where_email_password(email, password)

    success = False
    if signin_user is not None:
        flask_login.login_user(signin_user)
        success = True

    return json.dumps({
        "success": success,
    })

@app.route('/signup')
def signup():
    return render_template("signup.html", title="Signup")

@app.route("/me")
@flask_login.login_required
def me():
    current_user = flask_login.current_user
    return f"Hello, {current_user.email}"

@app.route('/api/signup', methods=["POST"])
def signup_API():
    email = request.form['email']
    password = request.form['password']

    user_temp = Users()
    user_temp.email = email
    user_temp.password = password
    success = True

    try:
        user_temp.create()
    except sqlalchemy.exc.IntegrityError:
        success = False
    finally:
        return json.dumps({
            "success": success,
        })

@app.route('/@<username>/<product_slug>')
def product(username, product_slug):
    return render_template("product.html", title="Product")