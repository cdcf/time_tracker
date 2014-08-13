__author__ = 'Cedric Da Costa Faro'

from flask import render_template
from . import main


# Welcome screen
@main.route('/')
def index():
    return render_template('main/index.html/')