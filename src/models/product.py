from src import db


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def get_shop(self):
        return models.Shop.query.filter_by(shop_id=self.shop_id)

    @staticmethod
    def where_id(id):
        return Product.query.filter_by(id=id).first()