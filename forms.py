from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from wtforms.validators import DataRequired, Length,NumberRange
from wtforms.fields.html5 import DateField

class EmployeeAddForm(FlaskForm):
    id = StringField('Id',validators=[DataRequired(),Length(min=2, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    id_card = StringField('Id_card', validators=[DataRequired(), Length(min=2, max=20)])
    position = StringField('Position', validators=[DataRequired(), Length(min=2, max=20)])
    save = SubmitField('Save')

class DeviceAddForm(FlaskForm):
    id = StringField('Id',validators=[DataRequired(),Length(min=2, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    serial = StringField('Serial', validators=[DataRequired(), Length(min=2, max=20)])
    brand = StringField('Brand', validators=[DataRequired(), Length(min=2, max=20)])
    type = StringField('Type', validators=[DataRequired(), Length(min=2, max=20)])
    date_buy = DateField('Date buy',validators=[DataRequired()], format="%Y-%m-%d")
    value = StringField('Value', validators=[DataRequired()])
    save = SubmitField('Save')

class BorrowForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max = 20)])