__author__ = 'Cedric Da Costa Faro'

from flask import Blueprint

users = Blueprint('users', __name__)

from . import routes