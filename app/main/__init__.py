__author__ = 'Cedric Da Costa Faro'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes, errors