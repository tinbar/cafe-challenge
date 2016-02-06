# application imports
import app 
db = app.db

import app_utilities
 
import models

##########################
##### REGISTER ###########
##########################

def user_name_valid_for_registration(user_name):
	user = db.session.query(models.User).filter_by(user_name=user_name).first()
	if user:
		return False
	return True

def register_user(form):
	user_name = form['user_name']
	password = form['password']
	email = form['email']
	first_name = form['first_name']
	last_name = form['last_name']
	salt = app_utilities.salt()
	hashed_password = app_utilities.hashed_password_with_salt(password, salt)
	try:
		user = models.User(
			user_name=user_name,
			password=hashed_password,
			salt=salt,
			email=email,
			first_name=first_name,
			last_name=last_name
			)
		db.session.add(user)
		db.session.commit()
		return {'registered' : True, 'user_id' : int(user.id)}
	except:
		{'registered' : False}

##########################
##### AUTHENTICATE #######
##########################

# This will be used for web login
def authenticate_user_with_password(user_name, password):
	user = db.session.query(models.User).filter_by(user_name=user_name).first()
	if user:
		current_hash = str(user.password)
		salt = str(user.salt)
		hashed_password = app_utilities.hashed_password_with_salt(password, salt)
		if current_hash == hashed_password:
			return {'authorized' : True, 'user_id' : int(user.id)}
	return {'authorized' : False}

# This will be used for logging in through mobile and then saving the mobile device id for api requests later
def authenticate_user_with_password_and_register_mobile_device_id(user_name, password, mobile_device_id):
	if authenticate_user_with_password(user_name, password):
		user = db.session.query(models.User).filter_by(user_name=user_name).first()
		if len(mobile_device_id):
			user.mobile_device_id = mobile_device_id
			db.session.commit()
			return {'authorized' : True}
	return {'authorized' : False}

# This will be used for api requests from mobile client after confirming a login
def authenticate_user_with_mobile_device_id(user_name, mobile_device_id):
	if not len(mobile_device_id):
		return False
	user = db.session.query(models.User).filter_by(
		user_name=user_name,
		mobile_device_id=mobile_device_id
		).first()
	if user:
		return True
	return False

### CONTACT ###

def insert_contact(form, user_id):
	first_name = form['first_name']
	last_name = form['last_name']
	email = form['email']
	phone_number = form['phone_number']
	try:
		contact = models.Contact(
			first_name=first_name,
			last_name=last_name,
			email=email,
			phone_number=phone_number,
			is_google_contact=False,
			user_id=user_id
			)
		db.session.add(contact)
		db.session.commit()
		return {'created' : True}
	except:
		{'created' : False}

def insert_google_contacts(google_contacts, user_id):
	pass

def all_contacts(user_id):
	contacts = models.Contact.query.filter_by(user_id=user_id)
	return contacts