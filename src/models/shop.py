from src import db
from src.models.product import Product
from src.models.transaction import Transaction


class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_email = db.Column(db.String)
    business_legality_id = db.Column(db.String)
    office_address = db.Column(db.String)
    website = db.Column(db.String)
    office_phone = db.Column(db.String)
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

    def get_order(self):
        product_id_list = list(map(lambda product: product.id, self.get_products()))
        #print(product_id_list)
        return list(filter(lambda transaction: transaction.product_id in product_id_list
                           and transaction.is_done is False, Transaction.all()))
