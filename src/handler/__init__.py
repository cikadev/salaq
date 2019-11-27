from flask import render_template, request, flash, url_for, redirect, send_from_directory
import sqlalchemy
import json
import flask_login
from src import login_manager, app

from src.models.users import Users
from src.models.product import Product
from src.models.shop import Shop
from src.models.media import Media
from src.models.trolley import Trolley


@login_manager.user_loader
def load_user(email):
    if email is not None:
        user = Users.where_email(email)
        user.shop = Shop.where_user_email(email)
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for("signin"))


@app.route('/')
def home():
    current_user = flask_login.current_user
    product_list = Product.query.all()

    def add_image(product):
        try:
            image = Media.where_product_id_image(product.id)[0]
            image_url = f"/dynamic/{image.type}/{image.url}"
        except IndexError:
            image_url = "https://bulma.io/images/placeholders/1280x960.png"
        return product, image_url

    product_list_and_media = map(add_image, product_list)
    return render_template("home.html", title="Home", product_list_and_media=product_list_and_media, current_user=current_user)


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

    media_3d = Media.where_product_id_3d(product_id)
    media_images = Media.where_product_id_image(product_id)

    print(media_3d)

    current_user = flask_login.current_user
    return render_template("product.html", title="Product", product=product, shop=shop, media_3d=media_3d,
                           media_images=media_images, current_user=current_user)


@app.route('/@<shop_id>')
def shop(shop_id):
    shop = Shop.where_id(shop_id)
    if shop is None:
        return redirect(url_for("not_found"))

    product_list = shop.get_products()

    def add_image(product):
        try:
            image = Media.where_product_id_image(product.id)[0]
            image_url = f"/dynamic/{image.type}/{image.url}"
        except IndexError:
            image_url = "https://bulma.io/images/placeholders/1280x960.png"
        return product, image_url

    product_list_and_media = map(add_image, product_list)

    return render_template("shop.html", title="Shop", shop=shop, product_list_and_media=product_list_and_media)

@app.route('/api/me/trolley')
@flask_login.login_required
def me_trolley_API():
    current_user = flask_login.current_user

    def add_product_name(trolley_product):
        product = Product.where_id(trolley_product.product_id);
        trolley_data = trolley_product.to_dict()
        trolley_data["name"] = product.name
        trolley_data["price"] = product.price
        return trolley_data

    return json.dumps({
        "trolley": list(map(add_product_name, Trolley.where_user_email(current_user.email))),
    })

@app.route('/api/me/trolley', methods=["POST"])
@flask_login.login_required
def add_to_trolley_API():
    current_user = flask_login.current_user

    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    trolley_temp = Trolley.where_user_email_and_product_id(current_user.email, product_id)
    if trolley_temp is not None:
        trolley_temp.quantity += quantity
        trolley_temp.update_quantity()
    else:
        trolley_temp = Trolley()
        trolley_temp.user_email = current_user.email
        trolley_temp.product_id = product_id
        trolley_temp.quantity = quantity
        trolley_temp.create()

    return json.dumps({
        "success": True,
    })

@app.route('/api/me/trolley', methods=["DELETE"])
@flask_login.login_required
def delete_from_trolley_API():
    current_user = flask_login.current_user

    product_id = request.form['product_id']

    trolley_temp = Trolley.where_user_email_and_product_id(current_user.email, product_id)
    if trolley_temp is not None:
        trolley_temp.delete()

    return json.dumps({
        "success": True,
    })

@app.route('/404')
def not_found():
    return "404"


@app.route('/dynamic/<path:filename>')
def custom_static(filename):
    return send_from_directory("dynamic/", filename)
