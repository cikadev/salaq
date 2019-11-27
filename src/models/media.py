from src import db


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    url = db.Column(db.String)
    product_id = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def get_shop(self):
        return models.Shop.query.filter_by(shop_id=self.shop_id).first()

    @staticmethod
    def where_product_id(product_id):
        return Media.query.filter_by(product_id=product_id).all()

    @staticmethod
    def where_product_id_3d(product_id):
        return Media.query.filter_by(product_id=product_id, type="3d").all()

    @staticmethod
    def where_product_id_image(product_id):
        return Media.query.filter_by(product_id=product_id, type="image").all()
