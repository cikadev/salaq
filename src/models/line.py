from __future__ import annotations
import datetime

from src import db
from src.models.transaction import Transaction


class Line(db.Model):
    __tablename__ = "line"
    id: int = db.Column(db.Integer, primary_key=True)
    user_email: str = db.Column(db.String)
    date: datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ship_address: str = db.Column(db.String)
    postal_code: str = db.Column(db.String)
    note: str = db.Column(db.String)
    courrier_type: str = db.Column(db.String)

    def create(self) -> None:
        db.session.add(self)
        db.session.commit()

    def get_transaction(self) -> [Transaction]:
        return Transaction.where_line_id(self.id)

    @staticmethod
    def where_user_email(email: str) -> [Line]:
        return Line.query.filter_by(user_email=email).all()

    @staticmethod
    def where_id(id: int) -> [Line]:
        return Line.query.filter_by(id=id).first()
