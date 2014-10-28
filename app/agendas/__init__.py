from flask import Blueprint

agendas = Blueprint('agendas', __name__)

from . import routes