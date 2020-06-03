from app import app
from flask import render_template, redirect, url_for
from app.forms import RegistrationForm, AuthorizationForm

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