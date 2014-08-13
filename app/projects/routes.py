__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from .. import db
from ..models import Project
from . import projects
from .forms import ProjectForm


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
        return redirect(url_for('projects.list'))
    return render_template('projects/edit_project.html/', form=form)


# We list here all projects
@projects.route('/list/', methods=['GET', 'POST'])
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.date.desc()).paginate(page,
                                                                      per_page=current_app.config['PROJECT_PER_PAGE'],
                                                                      error_out=False)
    project_list = pagination.items
    return render_template('projects/list.html/', projects=project_list, pagination=pagination)




# this function is used as basis to generate a project
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
        return redirect(url_for('projects.list'))
    form.from_model(project)
    return render_template('projects/edit_project.html', form=form)
