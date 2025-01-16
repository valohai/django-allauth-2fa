Welcome to django-allauth-2fa!
==============================

.. image:: https://github.com/valohai/django-allauth-2fa/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/valohai/django-allauth-2fa/actions/workflows/ci.yml

.. image:: https://codecov.io/gh/valohai/django-allauth-2fa/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/valohai/django-allauth-2fa

.. image:: https://readthedocs.org/projects/django-allauth-2fa/badge/?version=latest
    :target: https://django-allauth-2fa.readthedocs.io/

django-allauth-2fa adds `two-factor authentication`_ to
versions of `django-allauth`_ older than 0.58.0.

For newer versions, you should use django-allauth's `built-in MFA support`_.
Please see `issue #189`_ for more information.

django-allauth is a set of `Django`_ applications which help with
authentication, registration, and other account management tasks.

Source code
    http://github.com/percipient/django-allauth-2fa
Documentation
    https://django-allauth-2fa.readthedocs.io/

.. _two-factor authentication: https://en.wikipedia.org/wiki/Multi-factor_authentication
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _Django: https://www.djangoproject.com/
.. _built-in MFA support: https://docs.allauth.org/en/latest/mfa/introduction.html
.. _issue #189: https://github.com/valohai/django-allauth-2fa/issues/189

Features
--------

* Adds `two-factor authentication`_ views and workflow to `django-allauth`_.
* Supports Authenticator apps via a QR code when enabling 2FA.
* Supports single-use back-up codes.

Compatibility
-------------

django-allauth-2fa is _not_ compatible with django-allauth versions newer than
0.58.0.

django-allauth has a built-in MFA implementation since version 0.56.0,
which is likely preferable to this one.

django-allauth-2fa attempts to maintain compatibility with supported versions of
Django, django-allauth, and django-otp.

Current versions supported together is:

======== ============== ============== ========================
Django   django-allauth django-otp     Python
======== ============== ============== ========================
4.1      0.57.2         1.2            3.8, 3.9, 3.10, 3.11
4.2      0.57.2         1.2            3.8, 3.9, 3.10, 3.11
======== ============== ============== ========================

Contributing
------------

django-allauth-2fa was initially created by
`Víðir Valberg Guðmundsson (@valberg)`_, was maintained by
`Percipient Networks`_ for many years, and finally by
`Valohai`_.

Please feel free to contribute if you find django-allauth-2fa useful,
but do note that you should likely be using allauth.mfa instead.

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

Start contributing
''''''''''''''''''
Start by cloning the project with:

.. code-block:: bash

    git clone https://github.com/valohai/django-allauth-2fa.git

The project uses `hatch`_ for building and package management.
If you don't have hatch installed, you can do so by running:

.. code-block:: bash

    pip install hatch

Setup you virtual environment with hatch:

.. code-block:: bash

    hatch env create

Running tests
'''''''''''''

Tests can be run using `pytest <https://docs.pytest.org/en/6.2.x/>`_

.. code-block:: bash

    hatch run pytest

Running the test project
''''''''''''''''''''''''

The test project can also be used as a minimal example using the following:

.. code-block:: bash

    hatch run python manage.py migrate
    hatch run python manage.py runserver

.. _Víðir Valberg Guðmundsson (@valberg): https://github.com/valberg
.. _Percipient Networks: https://www.strongarm.io
.. _Valohai: https://valohai.com/
.. _the repository: http://github.com/valohai/django-allauth-2fa
.. _hatch: https://hatch.pypa.io/
