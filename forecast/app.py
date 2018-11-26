"""builds Flask.app for running application"""

import os

from flask import Flask

from forecast import auth, api
from forecast.extensions import db, jwt, migrate

import prosper.common.prosper_logging as p_logging

HERE = os.path.abspath(os.path.dirname(__file__))

def create_app(config=None, testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('forecast')

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_blueprints(app)

    return app

def configure_app(app, testing=False):
    """set configuration for application
    """
    # default configuration
    app.config.from_object('forecast.config.DefaultConfig')
    log_builder = p_logging.ProsperLogger(
        app.name,
        os.path.join(HERE, 'logs'),
    )

    if testing is True:
        # override with testing config
        app.config.from_object('forecast.config.Test')
        log_builder.configure_debug_logger()
    else:
        app.config.from_object('forecast.config.Production')
        # override with env variable, fail silently if not set
        #app.config.from_envvar('FORECAST_CONFIG', silent=True)
        # TODO: log_builder.configure_slack_logger()

    for handler in log_builder.logger.handlers:
        app.logger.addHandler(handler)

def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)

def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
