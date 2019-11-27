import flask_login
from src import db


class Users(flask_login.UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    name = db.Column(db.String)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return self.email

    @staticmethod
    def where_email(email):
        return Users.query.filter_by(email=email).first()

    @staticmethod
    def where_email_password(email, password):
        return Users.query.filter_by(email=email, password=password).first()