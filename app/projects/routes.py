from flask import render_template
from ..models import User
from . import projects


@projects.route('/')
def index():
    return render_template('projects/index.html/')


@projects.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('projects/user.html/', user=user)