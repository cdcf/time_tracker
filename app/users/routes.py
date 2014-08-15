__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_required, current_user
from .. import db
from ..models import User
from . import users
from .forms import ProfileForm, ChangePasswordForm


# last part first_or_404 will return a 404 status code if user tries to manually overwrite the user
# name in the url and that this user does not exist in the db
# We then display the list of projects created by that user.
@users.route('/user/<username>/')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('users/user.html/', user=user)


# We enable here a user to complete his user profile once he has logged in
@users.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('users.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('users/profile.html/', form=form)


# We enable users to update their password
@users.route('/change-password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password', 'danger')
    return render_template('users/profile.html/', form=form)
