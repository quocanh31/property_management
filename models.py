from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20))
    identity_card = db.Column(db.String(20))
    position = db.Column(db.String(20))
    child1 = db.relationship('Borrow', backref='borrower', lazy= True)


class Device(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20))
    serial = db.Column(db.String(30))
    brand = db.Column(db.String(20))
    type = db.Column(db.String(20))
    date_buy = db.Column(db.DateTime(20))
    value = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    child2 = db.relationship('Borrow', backref='device_borrow', lazy = True)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.String(20), db.ForeignKey('employee.id'))
    device_id = db.Column(db.String(20), db.ForeignKey('device.id'))
    date_borrow = db.Column(db.DateTime())
    date_return = db.Column(db.DateTime())
