from flask import Flask
from models import db
from api.history import app as history_api
from api.employee_manage import app as employee_mangage
from api.device_manage import app as device_manage
from api.authentication import app as auth
from api.borrow_manage import app as borrow_manage
from api.export import app as export
from api.log import app as log

app = Flask(__name__)
db.init_app(app)
app.config.from_pyfile('config.py')

app.register_blueprint(history_api)
app.register_blueprint(employee_mangage)
app.register_blueprint(device_manage)
app.register_blueprint(auth)
app.register_blueprint(borrow_manage)
app.register_blueprint(export)
app.register_blueprint(log)


if __name__ == '__main__':
    app.run()
