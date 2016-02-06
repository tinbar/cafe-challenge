from flask.ext.wtf import Form
from wtforms import StringField, TextField, PasswordField, BooleanField, DateField, TextAreaField, SelectField, validators
import datetime
#from wtforms.validators import DataRequired

class LoginForm(Form):
	user_name = TextField('user_name', [validators.Required()])
	password = PasswordField('password', [validators.Required()])

class RegistrationForm(Form):
	user_name = TextField('user_name', [validators.Required()])
	password = PasswordField('password', [validators.Required()])
	email = TextField('email', [validators.Required(), validators.Email()])
	first_name = TextField('first_name', [validators.Required()])
	last_name = TextField('last_name', [validators.Required()])

class ContactForm(Form):
	first_name = TextField('first_name', [validators.Required()])
	last_name = TextField('last_name', [validators.Required()])
	email = TextField('email', [validators.Required()])
	phone_number = TextField('phone_number', [validators.Required()])