from . import db
import datetime

class UserProfile(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    age = db.Column(db.String(80), unique=True)
    biography = db.Column(db.String(300), unique=True)
    image = db.Column(db.String(80), unique=True)
    gender = db.Column(db.String(80))
    created_on = db.Column(db.DateTime)
        
        
    def __init__(self, userid, first_name, last_name, username, age, biography, image, gender, created_on):
        self.userid = userid
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.age = age
        self.biography = biography
        self.image = image
        self.gender = gender
        self.created_on = created_on
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
        
class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
