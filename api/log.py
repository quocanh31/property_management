from flask import Blueprint, render_template

from models import device_log_change, employee_log_change

app = Blueprint(name = 'log', import_name = __name__)

@app.route('/log_change')
def log_change():
    device_logs = device_log_change.query.all()
    employee_logs = employee_log_change.query.all()
    return render_template('log_change.html', device_logs = device_logs , employee_logs =employee_logs)