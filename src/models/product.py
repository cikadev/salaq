from src import db


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    is_deleted = db.Column(db.Boolean)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def get_shop(self):
        return models.Shop.query.filter_by(is_deleted=False, shop_id=self.shop_id).first()

    @staticmethod
    def all():
        return Product.query.filter_by(is_deleted=False).all()

    @staticmethod
    def where_id(id):
        return Product.query.filter_by(is_deleted=False, id=id).first()

    def update(self):
        db.session.query(Product).filter_by(id=self.id).update({
            "name": self.name,
            "description": self.description,
            "price": self.price,
        })
        db.session.commit()