from flask import render_template, request, flash, url_for, redirect
import sqlalchemy
import json
import flask_login
from src import login_manager, app
from src.models.users import Users

@login_manager.user_loader
def load_user(email):
    if email is not None:
        return models.Users.where_email(email)
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
    name = request.form['name']

    user_temp = Users(email=email, name=name, password=password)
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

@app.route('/url')
def testlaunch():
    return render_template("upload.html", title="Upload")