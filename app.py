import os

from flask import Flask, Response, request, render_template, flash, redirect, session, url_for, json, make_response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

import models

@app.route('/')
def hello():
	return ''
	
if __name__ == '__main__':
	app.run()