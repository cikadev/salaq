import flask_login
from src import db
import src.models


class Shop(flask_login.UserMixin, db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_email = db.Column(db.String)

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_user_has_shop(email):
        return Shop.query.filter_by(user_email=email) is not None

    def get_products(self):
        return models.Product.query.filter_by(shop_id=self.id)

    @staticmethod
    def where_id(id):
        return Shop.query.filter_by(id=id).first()