import app

db = app.db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    mobile_device_id = db.Column(db.String())
    salt = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    contacts = db.relationship('Contact', cascade='all, delete, delete-orphan', backref='user')
    # To be used after user confirms through verification email sent out after registration
    # confirmed = db.Column(db.Boolean, default=False)
    # confirmed_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    phone_number = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<id {}>'.format(self.id)