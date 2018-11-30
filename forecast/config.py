"""Default configuration

Use env var to override
"""
import os
import warnings

import prosper.common.prosper_config as p_config
from . import exceptions

HERE = os.path.abspath(os.path.dirname(__file__))
LOCAL_CONFIG_PATH = os.path.join(HERE, 'config.j2')

def generate_secret_cfg(local_cfg_path=LOCAL_CONFIG_PATH, env_key='SECRET_CFG'):
    """Generate secrets from credentials file

    Args:
        local_cfg_path (str): path to config file
        env_key (str): envvar with path to secret cfg

    Returns:
        ProsperConfig: a ConfigParser-like object

    Raises:
        SecretMissing: Warns if no template found for

    """
    if not os.environ.get('SECRET_CFG', ''):
        warnings.warn('No SECRET_CFG given', exceptions.SecretMissing)
    else:
        return p_config.render_secrets(
            local_cfg_path,
            os.environ.get('SECRET_CFG', ''),
        )
class DefaultConfig(object):
    DEBUG = True
    SECRET_KEY = 'TODO'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/forecast.db'  # FIXME
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    LOCAL_CONFIG = p_config.ProsperConfig(LOCAL_CONFIG_PATH)

class Cli(DefaultConfig):
    LOCAL_CONFIG = generate_secret_cfg()
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{server}/forecast'.format(
        username=LOCAL_CONFIG.get_option('FORECAST', 'mysql_username'),
        password=LOCAL_CONFIG.get_option('FORECAST', 'mysql_password'),
        server=LOCAL_CONFIG.get_option('FORECAST', 'mysql_server')
    )
    print(SQLALCHEMY_DATABASE_URI)
    DEBUG = True
    JWT_LEEWAY = 3600

class Test(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True

# TODO: abc/metaclass for PROD/DEV secrets objects https://github.com/brettlangdon/flask-env
class Production(DefaultConfig):
    """pull production secrets from environ"""
    # TODO: this sucks
    LOCAL_CONFIG = generate_secret_cfg()
