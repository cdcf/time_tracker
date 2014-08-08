__author__ = 'Cedric Da Costa Faro'

from flask import render_template, current_app, request, redirect, url_for, flash
from flask.ext.login import login_user
from ..models import User
from . import auth
from app import db
from .forms import LoginForm, RegistrationForm


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html/', form=form)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if not current_app.config['DEBUG'] and not current_app.config['TESTING'] and not request.is_secure:
        return redirect(url_for('auth.login', _external=True, _scheme='https'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password.')
            return redirect(url_for('auth.login'))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('projects.index'))
    return render_template('auth/login.html/', form=form)