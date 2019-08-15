from flask import Blueprint, request, session, render_template, url_for
from werkzeug.utils import redirect

from models import Admin, db

app = Blueprint('auth', import_name=__name__)

@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.method =='POST':
        admin=Admin.query.filter_by(username=request.form['username'], password = request.form['password']).first()
        if admin is not None:
        # if request.form['password'] == 'password' and request.form['username'] == 'admin':
            admin.status = 1
            db.session.commit()

            session['logged_in'] = True
            return redirect(url_for('borrow_manage.home'))
    return render_template('login.html')



@app.route("/logout")
def logout():
    admin = Admin.query.filter_by(status =1).first()
    admin.status =0
    db.session.commit()
    session['logged_in'] = False
    return redirect(url_for('borrow_manage.home'))