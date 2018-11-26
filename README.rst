|Show Logo|

ProsperForecast 
===============

|Build Status| |Coverage Status| |Docs|

Flask App for generating experimental stock forecasts

Getting Started
---------------

.. code-block:: none

    git clone git@github.com:EVEprosper/ProsperForecast.git
    pip3 install -e .
    # TODO: docker launcher


Testing
-------

.. code-block:: none

    python setup.py test

Deployment
----------

TODO

Secrets
-------

App expects a ``credentials.cfg`` file to pass in secrets

.. code-block:: cfg

    credentials.cfg
    [logging]
        slack_webhook = 

    [forecast]
        rh_username =
        rh_password =


.. |Show Logo| image:: http://dl.eveprosper.com/podcast/logo-colour-17_sm2.png
   :target: http://eveprosper.com
.. |Build Status| image:: https://travis-ci.org/EVEprosper/ProsperForecast.svg?branch=master
    :target: https://travis-ci.org/EVEprosper/ProsperForecast
.. |Coverage Status| image:: https://coveralls.io/repos/github/EVEprosper/ProsperForecast/badge.svg?branch=master
    :target: https://coveralls.io/github/EVEprosper/ProsperForecast?branch=master
.. |Docs| image:: https://readthedocs.org/projects/prosperforecast/badge/?version=latest
   :target: http://prosperforecast.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status