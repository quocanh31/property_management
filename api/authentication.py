from flask import Blueprint, request, session, render_template, url_for
from werkzeug.utils import redirect

app = Blueprint('auth', import_name=__name__)

@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.method =='POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('borrow_manage.home'))
    return render_template('login.html')



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('borrow_manage.home'))