from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, TextField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



class ProfileForm(FlaskForm):
	csrf = True
	username = StringField('Username', validators=[InputRequired()])
	firstname = TextField('Firstname', validators= [DataRequired("Please enter your first name")])
	lastname = TextField('Lastname', validators= [DataRequired("Please enter your last name")])
	age = TextField('age', validators= [DataRequired("Please enter your age")])
	biography = TextAreaField('biography', validators= [DataRequired("Tell me a little about yourself")])
	image = FileField('image',validators=[FileAllowed(['png','jpg','jpeg','gif'], 'Only an image file allowed')])
	gender = SelectField(u'Gender', choices=[('M', 'Male'), ('F', 'Female')])
	submit = SubmitField(" Submit profile details ")
