Welcome to django-allauth-2fa!
==============================

.. image:: https://github.com/valohai/django-allauth-2fa/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/valohai/django-allauth-2fa/actions/workflows/ci.yml

.. image:: https://codecov.io/gh/valohai/django-allauth-2fa/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/valohai/django-allauth-2fa

.. image:: https://readthedocs.org/projects/django-allauth-2fa/badge/?version=latest
    :target: https://django-allauth-2fa.readthedocs.io/

django-allauth-2fa adds `two-factor authentication`_ to `django-allauth`_.
django-allauth is a set of `Django`_ applications which help with
authentication, registration, and other account management tasks.

Source code
    http://github.com/percipient/django-allauth-2fa
Documentation
    https://django-allauth-2fa.readthedocs.io/

.. _two-factor authentication: https://en.wikipedia.org/wiki/Multi-factor_authentication
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _Django: https://www.djangoproject.com/

Features
--------

* Adds `two-factor authentication`_ views and workflow to `django-allauth`_.
* Supports Authenticator apps via a QR code when enabling 2FA.
* Supports single-use back-up codes.

Compatibility
-------------

django-allauth-2fa attempts to maintain compatibility with supported versions of
Django, django-allauth, and django-otp.

Current versions supported together is:

======== ============== ============== ========================
Django   django-allauth django-otp     Python
======== ============== ============== ========================
3.2      0.41.0         1.0, 1.1       3.7, 3.8, 3.9, 3.10
4.0      0.41.0         1.0, 1.1       3.8, 3.9, 3.10
======== ============== ============== ========================

Contributing
------------

django-allauth-2fa was initially created by
`Víðir Valberg Guðmundsson (@valberg)`_, was maintained by
`Percipient Networks`_ for many years, and is now maintained by
`Valohai`_. Please feel free to contribute if you find
django-allauth-2fa useful!

#. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
#. If you feel uncomfortable or uncertain about an issue or your changes,
   feel free to email support@percipientnetworks.com and we will happily help you.
#. Fork `the repository`_ on GitHub to start making your changes to the
   **main** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature
   works as expected.
#. Send a pull request and bug the maintainer until it gets merged and
   published.

Running tests
'''''''''''''

Tests can be run using [pytest](https://docs.pytest.org/en/6.2.x/).

.. code-block:: bash

    pip install -r requirements-test.txt
    py.test

Running the test project
''''''''''''''''''''''''

The test project can also be used as a minimal example using the following:

.. code-block:: bash

    # Migrate the SQLite database first.
    DJANGO_SETTINGS_MODULE=tests.settings python manage.py migrate
    # Run the server with debug.
    DJANGO_SETTINGS_MODULE=tests.settings python manage.py runserver_plus
    # Run the shell.
    DJANGO_SETTINGS_MODULE=tests.settings python manage.py shell_plus

.. _Víðir Valberg Guðmundsson (@valberg): https://github.com/valberg
.. _Percipient Networks: https://www.strongarm.io
.. _Valohai: https://valohai.com/
.. _the repository: http://github.com/valohai/django-allauth-2fa
