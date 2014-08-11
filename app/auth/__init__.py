__author__ = 'Cedric Da Costa Faro'
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import routes