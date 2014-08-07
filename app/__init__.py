from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config


bootstrap = Bootstrap()

db = SQLAlchemy


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)

    from .projects import projects as projects_blueprint
    app.register_blueprint(projects_blueprint)

    return app