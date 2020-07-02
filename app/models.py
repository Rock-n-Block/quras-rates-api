from app import db


class XqcRate(db.Model):
    __tablename__ = 'xqc_rates'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    usd_rate = db.Column(db.Float)
    jpy_rate = db.Column(db.Float)
