"""wheel setup for ProsperForecast"""
import codecs
import importlib

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

__package_name__ = 'ProsperForecast'
__library_name__ = 'forecast'

def get_version(*args):
    """find __version__ for making package

    Args:
        package_name (str): path to _version.py folder (abspath > relpath)

    Returns:
        str: __version__ value

    """
    module = f'{".".join(args)}._version'
    package = importlib.import_module(module)

    version = package.__version__

    return version

class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    http://doc.pytest.org/en/latest/goodpractices.html#manual-integration

    """
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            f'--cov={__library_name__}',
            '--cov-report=term-missing',
            '--cov-config=.coveragerc',
        ]

    def run_tests(self):
        import shlex
        import pytest
        pytest_commands = []
        try:
            pytest_commands = shlex.split(self.pytest_args)
        except AttributeError:
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

class QuietTest(PyTest):
    """overrides to prevent webhook spam while developing"""
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            f'--cov={__library_name__}',
            '--cov-report=term-missing',
            '--cov-config=.coveragerc',
        ]

with codecs.open('README.rst', 'r', 'utf-8') as readme_fh:
    README = readme_fh.read()

setup(
    name=__package_name__,
    author='John Purcell',
    author_email='prospermarketshow@gmail.com',
    version=get_version(__library_name__),
    packages=find_packages(exclude=['tests']),
    description='Flask App for generating experimental stock forecasts',
    long_description=README,
    package=find_packages(),
    package_data={
        '': ['LICENSE', 'README.rst'],
        'forecast': ['version.txt', 'config.j2'],
    },
    python_requires='>=3.6',
    install_requires=[
    ## cookiecutter requirements ##
        'flask',
        'flask-sqlalchemy',
        'flask-restful',
        'flask-migrate',
        'flask-jwt-extended',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'python-dotenv',
        'passlib',
    ## Custom requirements ##
        'ProsperCommon',
        'ProsperDatareader',
        'fbprophet',
        'gunicorn',
        'python-dotenv',
    ],
    tests_require=[
        'pytest',
        'pytest-prosper',
        'docker',
        'coverage',
        'pytest_cov',
        'factory_boy',
        'pytest-factoryboy',
        'pytest-flask',
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': [
            'forecast = forecast.manage:cli'
        ]
    },
    extras_require={
        'dev': [
            'sphinx',
            'sphinxcontrib-napoleon',
            'rstcheck',
        ],
    },
    cmdclass={
        'test': PyTest,
    },
)
