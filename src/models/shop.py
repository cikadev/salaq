from src import db
from src.models.product import Product


class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_email = db.Column(db.String)
    shop = None

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_user_has_shop(email):
        return Shop.query.filter_by(user_email=email) is not None

    def get_products(self):
        return Product.query.filter_by(shop_id=self.id).all()

    @staticmethod
    def where_id(id):
        return Shop.query.filter_by(id=id).first()

    @staticmethod
    def where_user_email(user_email):
        return Shop.query.filter_by(user_email=user_email).first()