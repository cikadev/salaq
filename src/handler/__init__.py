from flask import render_template, request, flash, url_for, redirect, send_from_directory, session, send_file
import sqlalchemy
import json
import flask_login
import os
import zipfile
import shutil
import pdfkit
from functools import reduce
from datetime import datetime

from src import login_manager, app

from src.helpers.mail import Mail
from src.helpers.video_processing import VideoProcessing

from src.models.users import Users
from src.models.product import Product
from src.models.shop import Shop
from src.models.media import Media
from src.models.line import Line
from src.models.transaction import Transaction


def remove_recursive(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                remove_recursive(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

@login_manager.user_loader
def load_user(email):
    if email is not None:
        user: Users = Users.where_email(email)
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
    product_list = Product.all()

    def add_image(product):
        try:
            image = Media.where_product_id_image(product.id)[0]
            image_url = f"/dynamic/{image.type}/{image.url}"
        except IndexError:
            image_url = "https://bulma.io/images/placeholders/1280x960.png"

        shop = Shop.where_id(product.shop_id)
        return product, shop, image_url

    product_list_and_media = map(add_image, product_list)
    return render_template("home.html", title="Home", product_list_and_media=product_list_and_media,
                           current_user=current_user)


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
def api_signup():
    email: str = request.form['email']
    password: str = request.form['password']
    name: str = request.form['name']

    user_temp: Users = Users()
    user_temp.email = email
    user_temp.password = password
    user_temp.name = name
    success = True

    try:
        user_temp.create()
    except sqlalchemy.exc.IntegrityError:
        success = False
    finally:
        return json.dumps({
            "success": success,
        })


@app.route('/@<int:shop_id>/<int:product_id>')
def product(shop_id, product_id):
    shop = Shop.where_id(shop_id)
    if shop is None:
        return redirect(url_for("not_found"))

    product = Product.where_id(product_id)
    if product is None:
        return redirect(url_for("not_found"))

    media_3d = Media.where_product_id_3d(product_id)
    media_images = Media.where_product_id_image(product_id)

    current_user = flask_login.current_user

    try:
        is_mine = current_user.email == shop.user_email
    except Exception:
        is_mine = False

    return render_template("product.html", title="Product", product=product, shop=shop, media_3d=media_3d,
                           media_images=media_images, current_user=current_user, is_mine=is_mine)


@app.route('/@<int:shop_id>')
def shop(shop_id):
    current_user = flask_login.current_user

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

    try:
        is_mine = current_user.email == shop.user_email
    except Exception:
        is_mine = False

    return render_template("shop.html", title="Shop", shop=shop, product_list_and_media=product_list_and_media,
                           is_mine=is_mine)

@app.route('/api/deliver/<int:transaction_id>')
@flask_login.login_required
def delivered(transaction_id):

    transaction = Transaction.where_id(transaction_id)
    transaction.done()

    return json.dumps({
        "success": True,
    })

@app.route('/@<int:shop_id>/order')
def shop_order(shop_id):
    current_user = flask_login.current_user

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

    orders = shop.get_order()

    orders = list(map(lambda order: (
        order,
        Product.where_id(order.id),
        Line.where_id(order.line_id),
        Users.where_email(Line.where_id(order.line_id).user_email)
        ), orders))

    try:
        is_mine = current_user.email == shop.user_email
    except Exception:
        is_mine = False

    return render_template("order.html", title="Shop Order", shop=shop, orders=orders,
                           is_mine=is_mine)

@app.route("/checkout")
@flask_login.login_required
def checkout():
    current_user = flask_login.current_user
    trolley = session["trolley"]
    total_price = reduce(lambda acc, value: acc + (value["price"] * value["quantity"]), trolley.values(), 0)
    return render_template("checkout.html", current_user=current_user, trolley=trolley, total_price=total_price)


@app.route('/api/me/trolley')
def me_trolley_API():
    # Careful
    if session.get("trolley") is None:
        session["trolley"] = {}

    return json.dumps({
        "success": True,
        "trolley": session["trolley"],
    })


@app.route('/api/me/trolley', methods=["POST"])
def add_to_trolley_API():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    product_detail = Product.where_id(product_id)

    try:
        session["trolley"][product_id]["quantity"] += quantity
        if session["trolley"][product_id]["quantity"] <= 0:
            del session["trolley"][product_id]
    except KeyError:
        session["trolley"][product_id] = {}
        session["trolley"][product_id]["id"] = product_id
        session["trolley"][product_id]["quantity"] = quantity
        session["trolley"][product_id]["name"] = product_detail.name
        session["trolley"][product_id]["price"] = product_detail.price

    session.modified = True

    return json.dumps({
        "success": True,
    })


@app.route('/api/me/trolley', methods=["DELETE"])
def delete_from_trolley_API():
    product_id = request.form['product_id']

    trolley_temp = session["trolley"]
    try:
        del trolley_temp[product_id]
    except KeyError:
        return json.dumps({
            "success": False,
        })

    return json.dumps({
        "success": True,
    })


@app.route("/shop/create")
def shop_create():
    current_user = flask_login.current_user
    return render_template("createshop.html", title="Create Shop", current_user=current_user)


@app.route('/api/createshop', methods=["POST"])
def createshop_API():
    current_user = flask_login.current_user

    name = request.form['name']
    business_legality_id = request.form['business_legality_id']
    office_address = request.form['office_address']
    office_phone = request.form['office_phone']
    website = request.form['website']
    shop_temp = Shop()
    shop_temp.name = name
    shop_temp.business_legality_id = business_legality_id
    shop_temp.office_address = office_address
    shop_temp.office_phone = office_phone
    shop_temp.website = website
    shop_temp.user_email = current_user.email
    shop_temp.create()
    return json.dumps({
        "success": True,
    })


@app.route('/@<int:shop_id>/product/add')
@flask_login.login_required
def add_product(shop_id):
    try:
        current_user = flask_login.current_user
        if shop_id != str(current_user.shop.id):
            return redirect(url_for("not_found"))
    except AttributeError:  # If user doesnt have any shop
        return redirect(url_for("not_found"))

    return render_template("addproduct.html", title="Add Product", current_user=current_user, shop_id=shop_id)

@app.route('/api/@<int:shop_id>/product/add', methods=["POST"])
@flask_login.login_required
def add_product_API(shop_id):
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']

    try:
        current_user = flask_login.current_user
        if shop_id != str(current_user.shop.id):
            return json.dumps({
                "success": False,
            })
    except AttributeError:  # If user doesnt have any shop
        return json.dumps({
            "success": False,
        })

    product_temp = Product()
    product_temp.shop_id = shop_id
    product_temp.name = name
    product_temp.price = price
    product_temp.description = description
    product_temp.create()

    return json.dumps({
        "success": True,
        "product_id": product_temp.id,
    })

# @app.route('/@<shop_id>/<product_id>/media/manage')
# @flask_login.login_required
# def manage_media(shop_id, product_id):
#     try:
#         current_user = flask_login.current_user
#         if shop_id != str(current_user.shop.id):
#             return redirect(url_for("not_found"))
#     except AttributeError:  # If user doesnt have any shop
#         return redirect(url_for("not_found"))
#
#     product = Product.where_id(product_id)
#
#     if product is None:
#         return redirect(url_for("not_found"))
#
#     return render_template("product-setting.html", title="Manage Media", current_user=current_user, shop_id=shop_id, product=product)

@app.route('/api/@<int:shop_id>/<int:product_id>/media/image/add', methods=["POST"])
@flask_login.login_required
def product_media_image_add_API(shop_id, product_id):
    uploaded_image = request.files['image']

    try:
        current_user = flask_login.current_user
        print(shop_id, current_user.shop.id)
        if str(shop_id) != str(current_user.shop.id):
            return json.dumps({
                "success": False,
                "message": "Invalid shop",
            })
    except AttributeError:  # If user doesnt have any shop
        return json.dumps({
            "success": False,
            "message": "Invalid shop. You don't have any shop",
        })

    try:
        extension = uploaded_image.filename.split(".")[-1]
    except Exception:
        return json.dumps({
            "success": False,
            "message": "No extension",
        })

    media_temp = Media()
    media_temp.type = "image"
    media_temp.url = ""
    media_temp.product_id = product_id
    media_temp.create()

    file_path = f"{media_temp.id}.{extension}"
    uploaded_image.save("src/dynamic/image/" + file_path)

    media_temp.url = file_path
    media_temp.update()

    return json.dumps({
        "success": True,
        "message": "",
    })

@app.route('/api/@<int:shop_id>/<int:product_id>/media/3d/add', methods=["POST"])
@flask_login.login_required
def product_media_3d_add_API(shop_id, product_id):
    uploaded_image = request.files['image']

    try:
        current_user = flask_login.current_user
        print(shop_id, current_user.shop.id)
        if str(shop_id) != str(current_user.shop.id):
            return json.dumps({
                "success": False,
                "message": "Invalid shop",
            })
    except AttributeError:  # If user doesnt have any shop
        return json.dumps({
            "success": False,
            "message": "Invalid shop. You don't have any shop",
        })

    try:
        extension = uploaded_image.filename.split(".")[-1]
    except Exception:
        return json.dumps({
            "success": False,
            "message": "No extension",
        })

    if extension != "zip":
        return json.dumps({
            "success": False,
            "message": "Wrong extension",
        })
    uploaded_image.save(f"temp_extract/{uploaded_image.filename}")
    with zipfile.ZipFile(f"temp_extract/{uploaded_image.filename}", "r") as zipObj:
        zipObj.extractall("temp_extract/extracted/")

    media_temp = Media()
    media_temp.type = "3d"
    media_temp.url = ""
    media_temp.product_id = product_id
    media_temp.create()

    os.makedirs(f"src/dynamic/3d/{media_temp.id}")
    shutil.copytree("temp_extract/extracted/", f"src/dynamic/3d/{media_temp.id}")

    file_path: str = ""

    for filename in os.listdir("temp_extract/extracted/"):
        if filename.endswith(".gltf") or filename.endswith(".obj"):
            file_path = f"{media_temp.id}/{filename}"
            break

    media_temp.url = file_path
    media_temp.update()

    # remove
    remove_recursive("temp_extract")

    return json.dumps({
        "success": True,
        "message": "",
    })

@app.route('/api/@<int:shop_id>/<int:product_id>/update', methods=["POST"])
@flask_login.login_required
def product_update_API(shop_id, product_id):
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']

    try:
        current_user = flask_login.current_user
        print(shop_id, current_user.shop.id)
        if str(shop_id) != str(current_user.shop.id):
            return json.dumps({
                "success": False,
                "message": "Invalid shop",
            })
    except AttributeError:  # If user doesnt have any shop
        return json.dumps({
            "success": False,
            "message": "Invalid shop. You don't have any shop",
        })

    product = Product.where_id(product_id)
    product.name = name if name != "" else product.name
    product.description = description if description != "" else product.description
    product.price = price if price != "" else product.price
    product.update()

    return json.dumps({
        "success": True,
        "message": "",
    })

@app.route("/transaction")
@flask_login.login_required
def transaction():
    current_user = flask_login.current_user

    def with_product(line):
        return {
            "line": line,
            "transactions": list(map(lambda transaction: {
                "transaction": transaction,
                "product": transaction.get_product(),
            }, line.get_transaction()))
        }

    line = list(map(with_product, Line.where_user_email(current_user.email)))
    for i in range(0, len(line)):
        total = 0
        done = 0
        for j in line[i]["transactions"]:
            print(j)
            if j["transaction"].is_done:
                done += 1
            total += 1

        if done == total:
            line[i]["progress"] = "Done"
        else:
            line[i]["progress"] = f"{ done }/{ total }"
        line[i]["total_price"] = reduce(lambda acc, value: acc + (value["product"].price * value["transaction"].quantity), line[i]["transactions"], 0)

    context = {
        "current_user": current_user,
        "lines": line,
    }

    return render_template("transaction.html", **context)

@app.route("/api/purchase", methods=["POST"])
@flask_login.login_required
def purchase():
    post_data = request.get_json()

    courrier_type = post_data['courrier_type']
    ship_address = post_data['ship_address']
    note = post_data['note']
    postal_code = post_data['postal_code']

    current_user = flask_login.current_user
    trolley = session["trolley"]

    try:
        line_temp = Line()
        line_temp.user_email = current_user.email
        line_temp.note = note
        line_temp.postal_code = postal_code
        line_temp.ship_address = ship_address
        line_temp.courrier_type = courrier_type
        line_temp.create()
    except Exception:
        return json.dumps({
            "success": False,
        })

    body_mail = """
    You have purchase some item(s) in Salaq, here is your invoice
    
    <!DOCTYPE html>
    <html>
    <body>
    <h2>Invoice</h2>
    <table class="table is-fullwidth">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total Price</th>
            </tr>
        </thead>
        <tbody>
    """

    for product_key, product_value in trolley.items():
        transaction_temp = Transaction()
        transaction_temp.line_id = line_temp.id
        transaction_temp.product_id = product_key
        transaction_temp.quantity = product_value["quantity"]
        transaction_temp.is_done = False
        transaction_temp.create()

        body_mail += f"""
            <tr>
                <td>{product_value["id"]}</td>
                <td>{product_value["name"]}</td>
                <td>{product_value["quantity"]}</td>
                <td>Rp. {product_value["price"]}</td>
                <td>Rp, {product_value["quantity"] * product_value["price"]}</td>
            </tr>
            """

    body_mail += """
        </tbody>
    </table>
    </body>
    </html>
    """

    Mail.send(line_temp.user_email, "Salaq Invoice", body_mail)

    session["trolley"] = {}
    return json.dumps({
        "success": True,
    })

@app.route('/404')
def not_found():
    return "404"


@app.route('/dynamic/<path:filename>')
def custom_static(filename):
    return send_from_directory("dynamic/", filename)

@app.route("/convert")
def convert_video_to_3d():
    current_user = flask_login.current_user
    return render_template("convert.html", current_user=current_user)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

@app.route("/download/invoice/<int:line_id>")
def download_invoice_pdf(line_id):
    line = Line.where_id(line_id)

    body = """
        You have purchase some item(s) in Salaq, here is your invoice

        <!DOCTYPE html>
        <html>
        <body>
        <h2>Invoice</h2>
        <table class="table is-fullwidth">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Total Price</th>
                </tr>
            </thead>
            <tbody>
        """

    grand_total = 0
    for transaction in line.get_transaction():
        product = Product.where_id(transaction.id)
        body += f"""
                <tr>
                    <td>{transaction.id}</td>
                    <td>{product.name}</td>
                    <td>{transaction.quantity}</td>
                    <td>Rp. {product.price}</td>
                    <td>Rp, {transaction.quantity * product.price}</td>
                </tr>
                """
        grand_total += transaction.quantity * product.price

    body += f"""
            </tbody>
        </table>
        <h3>Grand Total: Rp. { grand_total }</h3>
        </body>
        </html>
        """
    pdfkit.from_string(body, "temp_line/temp.pdf")

    return send_file("../temp_line/temp.pdf")

@app.route("/api/convert", methods=["POST"])
def api_convert_video_to_3d():
    uploaded_image = request.files['file']
    extension = uploaded_image.filename.split(".")[-1]
    if not (extension == "mp4" or extension == "wav"):
        return json.dumps({
            "success": False,
            "message": "File type is not allowed",
        })

    # saving
    print("Saving")
    uploaded_image.save(f"temp_convert/video/video.{extension}")

    # create image from video
    print("Creating image from video")
    video_temp = VideoProcessing(f"temp_convert/video/video.{extension}")
    video_temp.to_images(to="temp_convert/images/")

    # do task
    print("Do task")
    if video_temp.meshroom(input="temp_convert/images/", output="temp/model/") != 0:
        return json.dumps({
            "success": False,
            "message": "Failed",
        })

    timestamp = datetime.timestamp(datetime.now())
    zipf = zipfile.ZipFile(f'src/dynamic/convert/{ timestamp }.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('temp_convert/model/', zipf)
    zipf.close()

    # remove
    remove_recursive("temp_convert")

    return json.dumps({
        "success": True,
        "message": f"/dynamic/convert/{ timestamp }.zip",
    })