django-allauth-2fa
==================

.. image:: https://travis-ci.org/percipient/django-allauth-2fa.svg?branch=master
    :target: https://travis-ci.org/percipient/django-allauth-2fa

django-allauth-2fa adds `two-factor authentication`_ to `django-allauth`_, a set
of `Django`_ applications which help with authentication, registration, and
other account management tasks.

.. _two-factor authentication: https://en.wikipedia.org/wiki/Multi-factor_authentication
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _Django: https://www.djangoproject.com/

Features
--------



Installation
------------

Install `django-allauth-2fa` with pip (note that this will install Django,
django-allauth, django-otp, qrcode and all of their requirements):

.. _django-otp: https://bitbucket.org/psagers/django-otp/
.. _qrcode: https://github.com/lincolnloop/python-qrcode

.. code-block:: bash

    pip install django-allauth-2fa

After all the pre-requisities are installed, django-allauth and django-otp must
be configured in your Django settings file. (Please check the
`django-allauth documentation`_ and `django-otp documentation`_ for more
in-depth steps on their configuration.)

.. _django-allauth documentation: https://django-allauth.readthedocs.io/en/latest/installation.html
.. _django-otp documentation: http://pythonhosted.org/django-otp/overview.html#installation

.. code-block:: python

    INSTALLED_APPS = (
        # Required by allauth.
        'django.contrib.sites',

        # Configure Django auth package.
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',

        # Enable allauth.
        'allauth',
        'allauth.account',

        # Configure the django-otp package.
        'django_otp',
        'django_otp.plugins.otp_totp',
        'django_otp.plugins.otp_static',

        # Enable two-factor auth.
        'allauth_2fa',
    )

    MIDDLEWARE_CLASSES = (
        # Configure Django auth package.
        'django.contrib.auth.middleware.AuthenticationMiddleware',

        # Configure the django-otp package. Note this must be after the
        # AuthenticationMiddleware.
        'django_otp.middleware.OTPMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        # Configure allauth.
        'django.core.context_processors.request',
        "allauth.account.context_processors.account",
    )

    # Set the allauth adapter to be the 2FA adapter.
    ACCOUNT_ADAPTER = 'allauth_2fa.adapter.OTPAdapter'

    # Configure your default site. See
    # https://docs.djangoproject.com/en/dev/ref/settings/#sites.
    SITE_ID = 1

After the above is configure, you must run migrations.

.. code-block:: bash

    python manage.py migrate

Finally, you must include the django-allauth-2fa URLs:

.. code-block:: python

    from django.conf.urls import include, url

    urlpatterns = [
        # Include the allauth and 2FA urls from their respective packages.
        url(r'^', include('allauth_2fa.urls')),
        url(r'^', include('allauth.urls')),
    ]

Contribute
----------

django-allauth-2fa was initially created by
`Víðir Valberg Guðmundsson (@valberg)`_, and is currently maintained by
`Percipient Networks`_. Please feel free to contribute if you find
django-allauth-2fa useful!

#. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
#. If you feel uncomfortable or uncertain about an issue or your changes,
   feel free to email support@percipientnetworks.com and we will happily help you.
#. Fork `the repository`_ on GitHub to start making your changes to the
   **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature
   works as expected.
#. Send a pull request and bug the maintainer until it gets merged and
   published.

.. _Víðir Valberg Guðmundsson (@valberg): https://github.com/valberg
.. _Percipient Networks: https://www.strongarm.io
.. _the repository: http://github.com/percipient/django-allauth-2fa
