from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField  
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

# DataRequired uses field_flags = ('required',) as default
# so the form cannot be submitted and the error massege cannot be raised.
DataRequired.field_flags = ();

class RegistrationForm(FlaskForm):
	username 			= StringField('Username', validators = [DataRequired(), Length(min=1, max=20)])
	email 				= StringField('Email', validators = [DataRequired(), Email(), Length(min=1, max=120)])
	password 			= PasswordField('Password', validators = [DataRequired(), Length(min=1, max=60)])
	confirm_password	= PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit 				= SubmitField('Sign Up!')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('This username is taken. Choose another one.')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('This email is taken. Choose another one.')
	
class AuthorizationForm(FlaskForm):
	email 		= StringField('Email', validators = [DataRequired(), Email()])
	password	= PasswordField('Password', validators = [DataRequired()])
	submit 		= SubmitField('Log In!')
	remember_me = BooleanField('Remember Me')

class CreateTaskForm(FlaskForm):
	title 	= StringField('Title', validators = [DataRequired(), Length(min=1, max=100)])
	content = TextAreaField('Content')
	submit	= SubmitField('Create!')