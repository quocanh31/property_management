import datetime

from flask import Blueprint, flash, url_for, session, render_template, request
from sqlalchemy import exc
from werkzeug.utils import redirect
from datetime import datetime
from models import Borrow, db, Employee, Device

app= Blueprint(name='borrow_manage', import_name=__name__)

data =[]

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))
    else:
        # page = request.args.get(get_page_parameter(), type=int, default=1)
        # devices = Device.query.paginate(page, 10 ,False)
        # pagination = Pagination(page=page,per_page=10, total=Device.query.count(),css_framework='bootstrap3')
        devices = Device.query.all()
        return render_template('device_list.html',devices = devices)


@app.route('/getID',methods=['POST'])
def getID():
    if request.method == 'POST':
        global data
        data = request.json
        #print(data)
    return "Ok"

@app.route('/borrow')
def borrow():
    employees = Employee.query.all()
    return render_template('borrow_add.html', employees=employees)

@app.route('/borrow_add/<id>',methods=['GET'])
def borrow_add(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))
    else:
        global data
        for device_id in data:
            device = Device.query.filter_by(id=device_id).first()
            device.status = 0
            borrower_id = id
            borrow_info = Borrow(borrower_id=borrower_id, device_id=device_id,
                                 date_borrow=datetime.today().strftime('%Y-%m-%d'))
            db.session.add(borrow_info)
            db.session.commit()
        flash('Add complete!','success')
        # return redirect('/borrow_list')
        return redirect(url_for('history_api.borrow_history', id = id))

@app.route('/device_return/<id>/')
def device_return(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        try:
            borrow = Borrow.query.filter_by(id=id).first_or_404()
            borrow.date_return = datetime.today().strftime('%Y-%m-%d')
            borrow.device_borrow.status = 1
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Failed to return!', 'danger')

        return redirect(url_for('history_api.borrow_history', id = borrow.borrower_id))

@app.route('/return_from_borrowing_list/<id>')
def return_from_borrowing_list(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        try:
            borrow = Borrow.query.filter_by(id=id).first_or_404()
            borrow.date_return = datetime.today().strftime('%Y-%m-%d')
            borrow.device_borrow.status = 1
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Failed to return!', 'danger')

        return redirect(url_for('history_api.borrowing_history', id = borrow.borrower_id))

@app.route('/return/<id>/')
def return_from_borrowlist(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        try:
            borrow = Borrow.query.filter_by(id=id).first_or_404()
            borrower_name = Borrow.query.filter_by(id=id).first_or_404().borrower.name
            borrow.date_return = datetime.today().strftime('%Y-%m-%d')
            borrow.device_borrow.status = 1
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Failed to return!', 'danger')

        return redirect(url_for('history_api.borrow_list'))

