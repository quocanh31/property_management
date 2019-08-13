from flask import Blueprint, session, render_template, url_for
from sqlalchemy import and_
from werkzeug.utils import redirect

from models import Borrow, Employee

app = Blueprint(name='history_api', import_name=__name__)

@app.route('/history_list/<id>')
def borrow_history(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))
    history = Borrow.query.filter_by(borrower_id=id).all()
    borrower=Employee.query.filter_by(id=id).first_or_404()
    borrower_name = borrower.name
    borrower_id = borrower.id
    id_card = borrower.identity_card
    status='All'
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # history = Borrow.query.filter_by(borrower_id=id).paginate(page, 100 , False)
    # pagination = Pagination(page=page, per_page=100, total=Borrow.query.filter_by(borrower_id=id).count(), css_framework='bootstrap3')
    return render_template('employee_borrow_list.html', borrowlist = history,borrower_name=borrower_name, borrower_id=borrower_id
                           ,id_card = id_card,status=status)

@app.route('/history_list/<id>/borrowing')
def borrowing_history(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))
    history = Borrow.query.filter_by(borrower_id=id, date_return= None).all()
    borrower=Employee.query.filter_by(id=id).first_or_404()
    borrower_name = borrower.name
    borrower_id = borrower.id
    id_card = borrower.identity_card
    status='Borrowing'
    return render_template('employee_borrow_list.html', borrowlist = history,borrower_name=borrower_name, borrower_id=borrower_id
                           ,id_card = id_card,status=status)

@app.route('/history_list/<id>/returned')
def returned_history(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))
    history = Borrow.query.filter(and_(Borrow.borrower_id == id, Borrow.date_return.isnot(None)))
    borrower=Employee.query.filter_by(id=id).first_or_404()
    borrower_name = borrower.name
    borrower_id = borrower.id
    id_card = borrower.identity_card
    return render_template('employee_borrow_list.html', borrowlist = history,borrower_name=borrower_name, borrower_id=borrower_id
                           ,id_card = id_card)

@app.route('/borrow_list')
def borrow_list():
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # borrowlist = Borrow.query.paginate(page, 1000, False)
    # pagination = Pagination(page=page, per_page=1000, total=Borrow.query.count(), css_framework='bootstrap3')
    borrowlist = Borrow.query.filter().order_by(Borrow.date_borrow.desc())
    return render_template('borrow_list.html', borrowlist = borrowlist)