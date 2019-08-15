from datetime import datetime

from flask import Blueprint, session, url_for, flash, render_template, request
from sqlalchemy import exc
from werkzeug.utils import redirect


from forms import DeviceAddForm
from models import Device, db, device_log_change, Admin

app = Blueprint(name = 'device_mange', import_name = __name__)

@app.route('/device/add', methods=['GET', 'POST'])
def DeviceAdd():
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:
        form = DeviceAddForm()
        if form.validate_on_submit():

            try:
                admin = Admin.query.filter_by(status =1).first()
                device = Device(id = form.id.data, name = form.name.data, serial =form.serial.data, brand =form.brand.data
                                ,type = form.type.data, date_buy = form.date_buy.data.strftime('%Y-%m-%d'), value = int(form.value.data.replace(',', '')), status =1,is_deleted=0)
                # db.session.delete(device)
                db.session.add(device)
                db.session.commit()

            except exc.SQLAlchemyError:
                flash('Failed to add!', 'danger')
                return redirect('/device/add')
            else:
                insert_device= device_log_change(device_id= device.id, name = device.name, serial =device.serial, brand = device.brand,
                                              type = device.type, date_buy= form.date_buy.data.strftime('%Y-%m-%d'), value = device.value,
                                              change_by =admin.username,date_change =datetime.now().strftime("%Y-%m-%d %H:%M[:%S[.%f]]"),note="", action ="Insert")
                db.session.add(insert_device)
                db.session.commit()
                flash('Add completed!', 'success')
                return redirect('/device/add')
        return render_template('device_add.html',form=form)




@app.route('/device/<id>/edit', methods =['GET', 'POST'])
def DeviceEdit(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

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
                admin = Admin.query.filter_by(status =1).first()
                edit_device= device_log_change(device_id= device.id+";"+form.id.data, name = device.name+";"+form.name.data, serial =device.serial+";"+form.serial.data,
                                                brand = device.brand +";"+form.brand.data,
                                                type = device.type+";"+form.type.data,
                                                date_buy= device.date_buy.strftime('%Y-%m-%d')+";"+form.date_buy.data.strftime('%Y-%m-%d'),
                                               value = str(device.value) +";"+ form.value.data.replace(',', ''),
                                                change_by =admin.username,date_change =datetime.now().strftime("%Y-%m-%d %H:%M[:%S[.%f]]"),note="", action ="Edit")
                device.id = form.id.data
                # print(form.id.data)
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
                db.session.add(edit_device)
                db.session.commit()
                flash('Edit completed!', 'success')
                return redirect((url_for('.DeviceEdit', id = device.id)))
        return render_template('device_edit.html',form = form)

@app.route('/device/<id>/delete/', methods=['GET','POST'])
def DeviceDelete(id):
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

    else:

        if request.method == 'POST':
            note= request.form['note']

            try:
                admin = Admin.query.filter_by(status =1).first()
                device = Device.query.filter_by(id=id).first_or_404()
                device.is_deleted = 1
                del_device= device_log_change(device_id= device.id, name = device.name, serial =device.serial, brand = device.brand,
                                              type = device.type, date_buy= device.date_buy.strftime('%Y-%m-%d'), value = device.value,
                                              change_by =admin.username,date_change =datetime.now().strftime("%Y-%m-%d %H:%M[:%S[.%f]]"),note=note, action ="Delete")
                db.session.add(del_device)
                # db.session.delete(device)
                db.session.commit()
                flash('Delete Success!', 'success')
            except exc.SQLAlchemyError:
                flash('Failed to delete!', 'danger')

            return redirect('/')

