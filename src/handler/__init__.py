from flask import render_template, request, flash, url_for, redirect, send_from_directory
import sqlalchemy
import json
import flask_login
from src import login_manager, app

from src.models.users import Users
from src.models.product import Product
from src.models.shop import Shop


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
    current_user = flask_login.current_user
    product_list = Product.query.all()
    print(product_list)
    return render_template("home.html", title="Home", product_list=product_list, current_user=current_user)

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

@app.route('/@<shop_id>/<product_id>')
def product(shop_id, product_id):
    shop = Shop.where_id(shop_id)
    if shop is None:
        return redirect(url_for("not_found"))

    product = Product.where_id(product_id)
    if product is None:
        return redirect(url_for("not_found"))

    return render_template("product.html", title="Product", product=product, shop=shop)

@app.route('/@<shop_id>')
def shop(shop_id):
    shop = Shop.where_id(shop_id)
    if shop is None:
        return redirect(url_for("not_found"))
    return render_template("shop.html", title="Shop", shop=shop)

@app.route('/404')
def not_found():
    return "404"

@app.route('/dynamic/<path:filename>')
def custom_static(filename):
    return send_from_directory("dynamic/", filename)
