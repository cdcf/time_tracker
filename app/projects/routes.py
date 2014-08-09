from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_required, current_user
from .. import db
from ..models import User, Project
from . import projects
from .forms import ProfileForm, ProjectForm


@projects.route('/')
def index():
    return render_template('projects/index.html/')


@projects.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('projects/user.html/', user=user)


@projects.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('projects.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('projects/profile.html/', form=form)


@projects.route('/new/', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(title=form.title.data,
                          description=form.description.data,
                          date=form.date.data,
                          author=current_user)
        db.session.add(project)
        db.session.commit()
        flash('The project was added successfully.')
        return redirect(url_for('projects.index'))
    return render_template('projects/edit_project.html/', form=form)