from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20))
    identity_card = db.Column(db.String(20))
    position = db.Column(db.String(20))
    is_deleted = db.Column(db.Boolean)
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
    is_deleted = db.Column(db.Boolean)
    child2 = db.relationship('Borrow', backref='device_borrow', lazy = True)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.String(20), db.ForeignKey('employee.id'))
    device_id = db.Column(db.String(20), db.ForeignKey('device.id'))
    date_borrow = db.Column(db.DateTime())
    date_return = db.Column(db.DateTime())


class Admin(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), primary_key=True)
    status = db.Column(db.Boolean)

class device_log_change(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id =db.Column(db.String(50))
    name = db.Column(db.String(50))
    serial = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    type = db.Column(db.String(50))
    date_buy = db.Column(db.String(50))
    value = db.Column(db.String(50))
    change_by =db.Column(db.String(20))
    date_change= db.Column(db.DateTime)
    note =db.Column(db.String(30))
    action = db.Column(db.String(20))

class employee_log_change(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id =db.Column(db.String(50))
    name = db.Column(db.String(50))
    identity_card = db.Column(db.String(50))
    position = db.Column(db.String(50))
    change_by =db.Column(db.String(20))
    date_change= db.Column(db.DateTime)
    note =db.Column(db.String(50))
    action = db.Column(db.String(20))

