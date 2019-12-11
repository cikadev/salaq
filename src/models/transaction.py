from src import db
from src.models.product import Product


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    is_done = db.Column(db.Boolean)

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all():
        return Transaction.query.all()

    def get_product(self):
        return Product.where_id(self.product_id)

    @staticmethod
    def where_id(id):
        return Transaction.query.filter_by(id=id).first()

    @staticmethod
    def where_line_id(line_id):
        return Transaction.query.filter_by(line_id=line_id).all()

    def done(self):
        db.session.query(Transaction).filter_by(id=self.id).update({
            "is_done": True,
        })
        db.session.commit()