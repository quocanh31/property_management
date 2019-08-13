from flask import Blueprint, render_template, session, url_for, flash,request
from sqlalchemy import exc
from werkzeug.utils import redirect

from forms import EmployeeAddForm
from models import Employee, db

app = Blueprint(name='employee_manage', import_name=__name__)

@app.route('/employee', methods=['GET', 'POST'])
def EmployeeList():
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        # page = request.args.get(get_page_parameter(), type=int, default=1)
        # employees = Employee.query.paginate(page, 1000 ,False)
        # pagination = Pagination(page=page,per_page=1000, total=Employee.query.count(),css_framework='bootstrap3')
        # return render_template('employee_list.html',employees = employees,pagination=pagination,)
        employees =  Employee.query.all()
        return render_template('employee_list.html', employees = employees)

@app.route('/employee/add', methods=['GET', 'POST'])
def EmployeeAdd():
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        form = EmployeeAddForm()
        if form.validate_on_submit():
            try:
                employee = Employee(id = form.id.data,name = form.name.data,identity_card = form.id_card.data,position = form.position.data)
                db.session.add(employee)
                db.session.commit()

            except exc.SQLAlchemyError:
                flash('Failed to add!', 'danger')
                return redirect('/employee/add')
            else:
                flash('Add completed!', 'success')
                return redirect('/employee/add')
        return render_template('employee_add.html',form=form)

@app.route('/employee/<id>/delete', methods=['GET'])
def EmployeeDelete(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        try:
            employee = Employee.query.filter_by(id=id).first_or_404()
            db.session.delete(employee)
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Failed to edit!', 'danger')
            return redirect('/employee')
        else:
            flash('Delete Success!', 'success')
            return redirect('/employee')

@app.route('/employee/<id>/edit', methods =['GET', 'POST'])
def EmployeeEdit(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        employee = Employee.query.filter_by(id=id).first_or_404()
        if request.method == 'POST':
            form = EmployeeAddForm(request.form)
        else:
            form = EmployeeAddForm()
            form.id.data = employee.id
            form.name.data = employee.name
            form.id_card.data = employee.identity_card
            form.position.data = employee.position
        if form.validate_on_submit():
            try:
                employee.id = form.id.data
                employee.name = form.name.data
                employee.identity_card = form.id_card.data
                employee.position = form.position.data
                db.session.commit()
            except exc.SQLAlchemyError:
                flash('Failed to edit!', 'danger')

                return redirect((url_for('.EmployeeEdit', id = employee.id)))
            else:
                flash('Edit completed!', 'success')
                return redirect((url_for('.EmployeeEdit', id = employee.id)))
        return render_template('employee_edit.html',form = form)