from flask import Blueprint, session, url_for, flash, render_template, request
from sqlalchemy import exc
from werkzeug.utils import redirect

from forms import DeviceAddForm
from models import Device, db

app = Blueprint(name = 'device_mange', import_name = __name__)

@app.route('/device/add', methods=['GET', 'POST'])
def DeviceAdd():
    if not session.get('logged_in'):
        return redirect(url_for('auth.do_admin_login'))

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
        return redirect(url_for('auth.do_admin_login'))

    else:
        try:
            device = Device.query.filter_by(id=id).first_or_404()
            db.session.delete(device)
            db.session.commit()
            flash('Delete Success!', 'success')
        except exc.SQLAlchemyError:
            flash('Failed to delete!', 'danger')

        return redirect('/')

