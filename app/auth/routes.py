__author__ = 'Cedric Da Costa Faro'

from flask import render_template, current_app, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from ..models import User
from . import auth
from app import db
from .forms import LoginForm, RegistrationForm


# We enable here new users to be registered in the app
@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login, remember to complete your profile.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html/', form=form)


# We first check that if we are in Production system, users have to be authenticated first.
# In any case, we define here the login page, and we check that both email and passwords are valid. We choose to
# work with passwords as they are unique values for a user.
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if not current_app.config['DEBUG'] and not current_app.config['TESTING'] and not request.is_secure:
        return redirect(url_for('auth.login', _external=True, _scheme='https'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('projects.index'))
    return render_template('auth/login.html/', form=form)


# We define here the logout process
@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('projects.index'))