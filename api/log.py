from flask import Blueprint, render_template, session, url_for, request
from flask_paginate import get_page_parameter, Pagination
from werkzeug.utils import redirect

from models import device_log_change, employee_log_change

app = Blueprint(name = 'log', import_name = __name__)

@app.route('/log_change')
def log_change():
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        # devices = Device.query.paginate(page, 10 ,False)
        # pagination = Pagination(page=page,per_page=10, total=Device.query.count(),css_framework='bootstrap3')
        device_logs = device_log_change.query.paginate(page, 3, False)
        employee_logs = employee_log_change.query.paginate(page, 3, False)
        pagination = Pagination(page=page, per_page=6, total=device_log_change.query.count() + employee_log_change.query.count(), css_framework='bootstrap3')
        return render_template('log_change.html', device_logs = device_logs , employee_logs =employee_logs, pagination =pagination)