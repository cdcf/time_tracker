__author__ = 'Cedric Da Costa Faro'

from datetime import datetime, date
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask.ext.login import UserMixin
from . import db, login_manager


# We define here user table with all required fields,
# we also retrieve user's avatar from Gravatar if any,
# We make sure that user's password is encrypted
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(128))
    bio = db.Column(db.Text())
    avatar_hash = db.Column(db.String(32))
    projects = db.relationship('Project', lazy='dynamic', backref='author')
    client = db.relationship('Client', lazy='dynamic', backref='author')
    agenda = db.relationship('Agenda', lazy='dynamic', backref='author')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# We define here the structure of the project table and link it to a user via a foreign key
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    date = db.Column(db.DateTime())
    agenda_id = db.relationship('Agenda', lazy='dynamic', backref='project_agenda')


# We define here the structure of the client table which will be re-used when creating projects.
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    projects = db.relationship('Project', lazy='dynamic', backref='client_project')


# We define here the structure of the agenda table which will be used to record an activity
# belonging to a project
class Agenda(db.Model):
    __tablename__ = 'agendas'
    id = db.Column(db.Integer, primary_key=True)
    agenda_date = db.Column(db.Date(), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
