from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, abort, Response
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url
from app.forms import RegistrationForm, AuthorizationForm, CreateTaskForm
from app.models import User, Task

@app.route('/')
def index():
	return redirect(url_for('register'))

@app.route('/authorization', methods=['GET', 'POST'])
def authorize():
	if current_user.is_authenticated:
		return redirect('account')
	else:
		form = AuthorizationForm()
		users = User.query.all()

		if form.validate_on_submit():

			user = User.query.filter_by(email = form.email.data).first()
			if user and bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember = form.remember_me.data)

				next = request.args.get('next')
				if next and is_safe_url(next, {'localhost:5000', '127.0.0.1:5000'}):
					return redirect(next)
				else: return redirect(url_for('account'))

			else:
				flash('Login Unsuccessful. Please check email and password')
				return redirect('account')

		else: return render_template('authorize.html', title = 'Authorization', form = form, users = users)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('authorize'))

@app.route('/registration', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect('account')
	else:
		form = RegistrationForm()
		

		if form.validate_on_submit():	
			password_hashed = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
			user = User(username = form.username.data, email = form.email.data, password = password_hashed)
			db.session.add(user)
			db.session.commit()
			flash('The user is successfully created.')
			return redirect(url_for('authorize'))

		else: return render_template('register.html', title = 'Registration', form = form)

@app.route('/remove_account')
def remove_account():
	user = User.query.filter_by(id = current_user.id).first()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('register'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = CreateTaskForm()
	tasks = Task.query.filter_by(user_id = current_user.id)

	if form.validate_on_submit():
		task = Task(title = form.title.data, content = form.content.data, author=current_user)
		db.session.add(task)
		db.session.commit()
		flash('The task is successfully created.')
		return redirect('account')
	else: return render_template('account.html', title = 'Account', form = form, tasks = tasks)

@app.route('/task/<int:task_id>')
@login_required
def task(task_id):
	task = Task.query.filter_by(id = task_id).first()

	if task:
		return render_template('task.html', task = task)
	else: 
		flash('The task does not exist.')
		return redirect(url_for('account'))

@app.route('/task/<int:task_id>/done')
@login_required
def done_task(task_id):
	task = Task.query.filter_by(id = task_id).first()

	if task:
		task.is_done = True
		db.session.commit()
		flash('The task is done now!')
		return redirect(url_for('account'))
	else:
		flash('The task does not exist.')
		return redirect(url_for('account'))

@app.route('/task/<int:task_id>/update')
@login_required
def update_task(task_id):
	pass

@app.route('/task/<int:task_id>/remove')
@login_required
def remove_task(task_id):
	task = Task.query.filter_by(id = task_id).first()

	if task:
		db.session.delete(task)
		db.session.commit()
		flash('The task is successfully deleted.')
		return redirect(url_for('account'))
	else:
		flash('The task does not exist.')
		return redirect(url_for('account'))

