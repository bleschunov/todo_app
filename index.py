from flask import Flask, render_template, redirect, url_for
from forms import RegistrationForm, AuthorizationForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c4e928aed3d42753f492642344712767'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
db = SQLAlchemy(app) 

class User(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False, default = 'default_ava.jpg')
	password = db.Column(db.String(60), nullable = False)
	tasks = db.relationship('Task', backref = 'author', lazy = True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Task(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	is_done = db.Column(db.Boolean, nullable = False, default = False)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

	def __repr__(self):
		return f"Task('{self.title}', '{self.date_posted}', 'Is done: {self.is_done}')"


@app.route('/')
def index():
	return redirect(url_for('register'))

@app.route('/authorization')
def authorize():
	form = AuthorizationForm()
	return render_template('authorize.html', title = 'Authorization', form = form)

@app.route('/registration')
def register():
	form = RegistrationForm()
	return render_template('register.html', title = 'Registration', form = form)

if __name__ == '__main__':
	app.run(debug = True)