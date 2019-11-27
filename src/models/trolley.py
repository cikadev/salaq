from src import db


class Trolley(db.Model):
    __tablename__ = 'trolley'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "user_email": self.user_email,
            "quantity": self.quantity,
            "product_id": self.product_id,
        }

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def where_user_email(user_email):
        return Trolley.query.filter_by(user_email=user_email).all()

    @staticmethod
    def where_user_email_and_product_id(user_email, product_id):
        return Trolley.query.filter_by(user_email=user_email, product_id=product_id).first()

    def update_quantity(self):
        db.session.query(Trolley).filter_by(user_email=self.user_email, product_id=self.product_id).update({
            "quantity": self.quantity,
        })
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

