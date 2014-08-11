from flask import render_template, flash, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from .. import db
from ..models import User, Project
from . import projects
from .forms import ProfileForm, ProjectForm


# When accessing the app, we want to see the list of existing projects
@projects.route('/')
def index():
    project_list = Project.query.order_by(Project.date.desc()).all()
    return render_template('projects/index.html/', projects=project_list)


# last part first_or_404 will return a 404 status code if user tries to manually overwrite the user
# name in the url and that this user does not exist in the db
# We then display the list of projects created by that user.
@projects.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    project_list = user.projects.order_by(Project.date.desc()).all()
    return render_template('projects/user.html/', user=user, projects=project_list)


# We enable here a user to complete his user profile once he has logged in
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
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('projects.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('projects/profile.html/', form=form)


# We allow here a user to create a new project once he has logged in and to modify his own ones only
@projects.route('/new/', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(author=current_user)
        form.to_model(project)
        db.session.add(project)
        db.session.commit()
        flash('The project was added successfully.', 'success')
        return redirect(url_for('projects.index'))
    return render_template('projects/edit_project.html/', form=form)


# We list here all projects
@projects.route('/project/<int:id>/')
def project(id):
    project = Project.query.get_or_404(id)
    headers = {}
    if current_user.is_authenticated():
        headers['X-XSS-Protection'] = '0'
    return render_template('projects/project.html/', project=project), 200, headers


# We enable project owner to edit them if required
@projects.route('/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if not current_user.is_admin and project.author != current_user:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        form.to_model(project)
        db.session.add(project)
        db.session.commit()
        flash('The project was updated successfully.', 'success')
        return redirect(url_for('projects.project', id=project.id))
    form.from_model(project)
    return render_template('projects/edit_project.html', form=form)