# python imports
import base64
import os
import hashlib

def salt():
	return base64.b32encode(os.urandom(32)).decode('utf-8')

def hashed_password_with_salt(password, salt):
	salt_password = salt.encode('utf-8') + password.encode('utf-8')
	hashed_password = hashlib.sha256(salt_password).hexdigest()
	return hashed_password