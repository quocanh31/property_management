from datetime import datetime

from flask import Blueprint, session, url_for, render_template, make_response
import pdfkit
from werkzeug.utils import redirect
config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

from models import Borrow, Employee

app = Blueprint('export_api', import_name=__name__)

@app.route('/export/<id>/')
def export(id):
    options = {
        'page-size': 'A4',
        'dpi': 400,
        'encoding': 'utf-8',
        'margin-top': '1.6cm',
        'margin-bottom': '2.54cm',
        'margin-left': '2.54cm',
        'margin-right': '2.54cm'
    }
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))
    borrows = Borrow.query.filter_by(borrower_id=id,date_return = None).all()
    borrower=Employee.query.filter_by(id=id).first_or_404()
    borrower_name = borrower.name
    id_card = borrower.identity_card
    currentDay = datetime.now().strftime('%d')
    currentMonth = datetime.now().strftime('%m')
    currentYear = datetime.now().strftime('%Y')
    rendered = render_template('export.html', borrows = borrows,name = borrower_name, id_card=id_card
                               ,currentDay = currentDay, currentMonth = currentMonth,currentYear = currentYear)
    pdf = pdfkit.from_string(rendered,False, configuration=config,options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Dispotition'] ='inline; filename=output.pdf'
    return response