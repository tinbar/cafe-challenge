#########################
# python imports
#########################

import os

#########################
# flask/web imports
#########################

from flask import Flask, request, Response, render_template, flash, redirect, session, url_for, json, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy.exc

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
def hello():
	return render_template('base.html')


##############################################################################
##############################################################################
##############  ADDRESS BOOK APPLICATION #####################################
##############################################################################
##############################################################################

@app.route('/register_user', methods = ['GET', 'POST'])
def register_user():
	if 'session_username' in session:
		return redirect('/')
	form = forms.RegistrationForm(request.form)
	if form.validate_on_submit() and request.method == 'POST':
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
	return render_template('register.html', form=form)

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


##############################################################################
##############################################################################
##############  ADDRESS BOOK API #############################################
##############################################################################
##############################################################################
	
if __name__ == '__main__':
	app.run()