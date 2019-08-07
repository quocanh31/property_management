from run import app
from models import Employee,Device,Borrow
from flask import render_template, flash, redirect, url_for, request,session,make_response
from forms import *
from run import db
from sqlalchemy import exc
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
import pdfkit

data =[]

@app.route('/borrow_list')
def borrow_list():
    if not session.get('logged_in'):
        return render_template('login.html')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    borrowlist = Borrow.query.paginate(page, 100, False)
    pagination = Pagination(page=page, per_page=100, total=Borrow.query.count(), css_framework='bootstrap3')
    return render_template('borrow_list.html', borrowlist = borrowlist, pagination = pagination)

@app.route('/history_list/<id>/<borrower_name>')
def borrow_history(id,borrower_name):
    if not session.get('logged_in'):
        return render_template('login.html')
    history = Borrow.query.filter_by(borrower_id=id,date_return = None).all()
    borrower_name = Employee.query.filter_by(id=id).first_or_404().name
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # history = Borrow.query.filter_by(borrower_id=id).paginate(page, 100 , False)
    # pagination = Pagination(page=page, per_page=100, total=Borrow.query.filter_by(borrower_id=id).count(), css_framework='bootstrap3')
    return render_template('employee_borrow_list.html', borrowlist = history,borrower_name=borrower_name)

@app.route('/device_return/<id>/')
def device_return(id):
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        try:
            borrow = Borrow.query.filter_by(id=id).first_or_404()
            borrower_name = Borrow.query.filter_by(id=id).first_or_404().borrower.name
            borrow.date_return = datetime.today().strftime('%Y-%m-%d')
            borrow.device_borrow.status = 1
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Failed to return!', 'danger')

        return redirect(url_for('borrow_history', id = borrow.borrower_id, borrower_name = borrower_name))

@app.route('/return/<id>/')
def return_from_borrowlist(id):
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        try:
            borrow = Borrow.query.filter_by(id=id).first_or_404()
            borrower_name = Borrow.query.filter_by(id=id).first_or_404().borrower.name
            borrow.date_return = datetime.today().strftime('%Y-%m-%d')
            borrow.device_borrow.status = 1
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Failed to return!', 'danger')

        return redirect(url_for('borrow_list'))


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
        return render_template('login.html')
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
        return redirect('/borrow_list')



@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        devices = Device.query.paginate(page, 1000 ,False)
        pagination = Pagination(page=page,per_page=1000, total=Device.query.count(),css_framework='bootstrap3')
        # devices = Device.query.paginate(page,2,False)
        # pagination = Pagination(page = page, total= Device.query.count())
        return render_template('device_list.html',devices = devices,pagination=pagination,)

@app.route('/borrow', methods=['GET','POST'])
def BorrowAdd():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        form = BorrowForm()
        if form.validate_on_submit():
            name = form.name.data
            borrower = Employee.query.filter_by(name=name).first()
            if borrower is None:
                flash('User not exist!', 'danger')
                return redirect('/borrow')
            else:
                for device_id in data:
                    device = Device.query.filter_by(id=device_id).first()
                    device.status = 0
                    borrower_id = borrower.id
                    print(borrower_id)
                    print(device_id)
                    borrow_info = Borrow(borrower_id= borrower_id, device_id = device_id,
                                         date_borrow= datetime.today().strftime('%Y-%m-%d'))
                    db.session.add(borrow_info)
                    db.session.commit()
                flash('Add completed!', 'success')
                return redirect('/borrow')
        return render_template('borrow.html', form=form)



@app.route('/device/add', methods=['GET', 'POST'])
def DeviceAdd():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        form = DeviceAddForm()
        if form.validate_on_submit():

            try:
                device = Device(id = form.id.data, name = form.name.data, serial =form.serial.data, brand =form.brand.data
                                ,type = form.type.data, date_buy = form.date_buy.data.strftime('%Y-%m-%d'), value = int(form.value.data.replace(',', '')), status =1)
                db.session.add(device)
                db.session.commit()

            except exc.SQLAlchemyError:
                flash('Failed to add!', 'danger')
                return redirect('/device/add')
            else:
                flash('Add completed!', 'success')
                return redirect('/device/add')
        return render_template('device_add.html',form=form)


@app.route('/employee/<id>/edit', methods =['GET', 'POST'])
def EmployeeEdit(id):
    if not session.get('logged_in'):
        return render_template('login.html')

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

@app.route('/device/<id>/edit', methods =['GET', 'POST'])
def DeviceEdit(id):
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        device = Device.query.filter_by(id=id).first_or_404()
        if request.method == 'POST':
            form = DeviceAddForm(request.form)
        else:
            form = DeviceAddForm()
            form.id.data = device.id
            form.name.data = device.name
            form.serial.data = device.serial
            form.brand.data = device.brand
            form.type.data = device.type
            form.date_buy.data = device.date_buy
            form.value.data = str(device.value)
        if form.validate_on_submit():
            try:
                device.id = form.id.data
                print(form.id.data)
                device.name = form.name.data
                device.serial = form.serial.data
                device.brand = form.brand.data
                device.type = form.type.data
                device.date_buy = form.date_buy.data.strftime('%Y-%m-%d')
                device.value = int(form.value.data.replace(',', ''))
                db.session.commit()

            except exc.SQLAlchemyError:
                flash('Failed to edit!', 'danger')

                return redirect((url_for('.DeviceEdit', id = device.id)))
            else:
                flash('Edit completed!', 'success')
                return redirect((url_for('.DeviceEdit', id = device.id)))
        return render_template('device_edit.html',form = form)

@app.route('/device/<id>/delete', methods=['GET'])
def DeviceDelete(id):
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        try:
            device = Device.query.filter_by(id=id).first_or_404()
            db.session.delete(device)
            db.session.commit()
            flash('Delete Success!', 'success')
        except exc.SQLAlchemyError:
            flash('Failed to delete!', 'danger')

        return redirect('/')

@app.route('/employee', methods=['GET', 'POST'])
def EmployeeList():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        employees = Employee.query.paginate(page, 20 ,False)
        pagination = Pagination(page=page,per_page=20, total=Employee.query.count(),css_framework='bootstrap3')
        # devices = Device.query.paginate(page,2,False)
        # pagination = Pagination(page = page, total= Device.query.count())
        return render_template('employee_list.html',employees = employees,pagination=pagination,)
        # employees =  Employee.query.all()
        # return render_template('employee_list.html', employees = employees)

@app.route('/employee/add', methods=['GET', 'POST'])
def EmployeeAdd():
    if not session.get('logged_in'):
        return render_template('login.html')

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
        return render_template('login.html')

    else:
        employee = Employee.query.filter_by(id=id).first_or_404()
        db.session.delete(employee)
        db.session.commit()
        flash('Delete Success!', 'success')
        return redirect('/employee')
