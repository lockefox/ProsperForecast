"""Default configuration

Use env var to override
"""
import os

import prosper.common.prosper_config as p_config

HERE = os.path.abspath(os.path.dirname(__file__))
LOCAL_CONFIG_PATH = os.path.join(HERE, 'config.j2')

class DefaultConfig(object):
    DEBUG = True
    SECRET_KEY = 'TODO'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/forecast.db'  # FIXME
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    LOCAL_CONFIG = p_config.ProsperConfig(LOCAL_CONFIG_PATH)

class Test(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True


# TODO: abc/metaclass for PROD/DEV secrets objects https://github.com/brettlangdon/flask-env
class Production(DefaultConfig):
    """pull production secrets from environ"""
    # TODO: this sucks
    LOCAL_CONFIG = p_config.render_secrets(
        LOCAL_CONFIG_PATH,
        os.environ.get('SECRET_CFG', ''),
    )
