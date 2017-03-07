from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, TextField, SelectField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename


class ProfileForm(FlaskForm):
	csrf = True
	firstname = TextField('Firstname', validators= [DataRequired("Please enter your first name")])
	lastname = TextField('Lastname', validators= [DataRequired("Please enter your last name")])
	age = TextField('age', validators= [DataRequired("Please enter your age")])
	biography = TextAreaField('biography', validators= [DataRequired("Tell me a little about yourself")])
	image = FileField('image',validators=[FileRequired()])
	gender = SelectField(u'Gender', choices=[('M', 'Male'), ('F', 'Female')])
	submit = SubmitField(" Submit profile details ")
