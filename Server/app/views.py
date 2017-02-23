from flask import render_template, session, redirect, flash, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, models, login_manager
from .forms import LoginForm
import datetime as dt
import sys
import logging

##Default logging posts
logging.basicConfig(filename='wonderLand.log',level=logging.DEBUG)
logging.info('Application launched on '+dt.datetime.today().strftime("%m/%d/%Y"))

##This callback is used to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(id):
	return models.User.query.get(id)

##The login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = models.User.query.filter_by(username = request.form['username']).first()
		if user is not None and (user.password == request.form['password']):
			login_user(user)
			flash('Logged in succesfully')
			return redirect('/loggedIn')
		else:
			flash('Invalid Credentials. Please Try Again')
	return render_template('login.html', form = form)


##logging the user out
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/login')

##Once user is logged page is displayed
@app.route('/loggedIn')
def index():
    return render_template('loggedIn.html')
