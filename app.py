#########################
# python imports
#########################

import os

#########################
# flask/web imports
#########################

from flask import Flask, request, Response, render_template, flash, redirect, session, url_for, json, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.api import status
import sqlalchemy.exc
import jsonpickle

#########################
# config app and database
#########################

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

#########################
# application imports
#########################

# import web_routes
# import mobile_api_routes
import database
import forms

@app.route('/')
def index():
	return render_template('base.html')


##############################################################################
##############################################################################
##############  ADDRESS BOOK APPLICATION #####################################
##############################################################################
##############################################################################


### USER ####

@app.route('/register_user', methods = ['GET', 'POST'])
def register_user():
	if 'session_username' in session:
		return redirect('/')
	registration_form = forms.RegistrationForm(request.form)
	if registration_form.validate_on_submit() and request.method == 'POST':
		user_name = request.form['user_name']
		if database.user_name_valid_for_registration(user_name):
			user_registration = database.register_user(request.form)
			if user_registration['registered']:
				session['session_username'] = user_name
				session['session_user_id'] = user_registration['user_id']
				return redirect('/')
			else:
				flash('Sorry, there seems to have been a problem with the database! Bad values, probably.')
				return redirect('/register_user')
				# flash good user name but db issue
		else:
			flash('Sorry, that user name is taken, try another!')
			return redirect('/register_user')
		# flash bad username message
		# should actually be done with ajax call that checks valid username as user inputs text
		# 
	# GET
	return render_template('register.html', form=registration_form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if 'session_username' in session:
		return redirect('/')
	login_form = forms.LoginForm(request.form)
	if login_form.validate_on_submit() and request.method == 'POST':
		user_name = request.form['user_name']
		password = request.form['password']
		user_authorization = database.authenticate_user_with_password(user_name, password)
		if user_authorization['authorized']:
			session['session_username'] = user_name
			session['session_user_id'] = user_authorization['user_id']
			return redirect('/')
	# GET the form
	return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
	session.pop('session_username', None)
	session.pop('session_user_id', None)
	return redirect('/')

### CONTACTS ###

# Get the contacts from the database and prepare the collection
def get_contacts_json():
	if not 'session_username' in session:
		return {}
	contacts_query = database.all_contacts(session['session_user_id'])
	contacts = list(contacts_query.all())
	casted = []
	for contact in contacts:
		current = {}
		for k in contact.__table__.columns:
			key = k.name
			current[key] = str(getattr(contact, key))
		casted.append(current)
	return casted

# GET : Read all contacts
@app.route('/contacts')
def get_contacts():
	contacts_json = get_contacts_json()
	response = make_response((jsonpickle.encode(contacts_json), 200))
	response.mimetype = 'application/json'
	return response

# POST : Create a new contact
@app.route('/contacts', methods = ['POST'])
def create_contact():
	if not 'session_username' in session:
		return redirect('/')
	contact_form = forms.ContactForm(request.form)
	if contact_form.validate_on_submit() and request.method == 'POST':
		contact_insertion = database.insert_contact(request.form, session['session_user_id'])
		response = make_response((jsonpickle.encode(contact_insertion), 201))
		response.mimetype = 'application/json'
		return response

# PATCH : Edit/Update an existing contact
@app.route('/contacts', methods = ['PATCH'])
def update_contact():
	if not 'session_username' in session:
		return redirect('/')
	contact_form = forms.ContactForm(request.form)
	print(contact_form)
	if contact_form.validate():
		contact_update = database.update_contact(request.form)
		response = make_response((jsonpickle.encode(contact_update), 200))
		response.mimetype = 'application/json'
		return response
	else:
		print(contact_form.errors)

# DELETE : Delete an existing contact
@app.route('/contacts', methods = ['DELETE'])
def delete_contact():
	if not 'session_username' in session:
		return redirect('/')
	contact_id = request.form['contact_id']
	contact_delete = database.delete_contact(contact_id)
	response = make_response((jsonpickle.encode(contact_delete), 200))
	response.mimetype = 'application/json'
	return response

# HTML Page to handle routing to various end points
@app.route('/contacts.html')
def contacts_html():
	if not 'session_username' in session:
		return redirect('/')
	# some id exists, meaning either create new or edit existing, don't just get all
	if request.args.get("id") is not None:
		request_id = request.args.get("id")
		contact_form = forms.ContactForm(request.form)
		# if it's new, just return the form
		if str(request_id) == "new":
			return render_template('contact.html', form=contact_form, header_text='Insert Contact', submit_text='Create', method='post')
		# otherwise, try to get a contact model using the id
		try:
			id_num = int(request_id)
			contact = database.get_contact_with_id(id_num)
			# if no such contact, raise an error and the except will take care of the 404
			if not contact:
				raise 'No such contact'
			contact_form.first_name.data = contact.first_name
			contact_form.last_name.data = contact.last_name
			contact_form.email.data = contact.email
			contact_form.phone_number.data = contact.phone_number
			return render_template('contact.html', form=contact_form, header_text='Edit Contact', submit_text='Update', contact_id=id_num, method='patch')
		# if it fails, 404
		except:
			response = make_response(("", 404))
			return response
	# if it hasn't terminated by now, it means get all contacts
	contacts = get_contacts_json()
	return render_template('contacts.html', contacts=contacts)


##############################################################################
##############################################################################
##############  ADDRESS BOOK API #############################################
##############################################################################
##############################################################################
	
if __name__ == '__main__':
	app.run()