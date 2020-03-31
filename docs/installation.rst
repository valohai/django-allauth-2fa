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
.. _django-otp documentation: https://django-otp-official.readthedocs.io/en/latest/overview.html#installation

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

        # Reset login flow middleware. If this middleware is included, the login
        # flow is reset if another page is loaded between login and successfully
        # entering two-factor credentials.
        'allauth_2fa.middleware.AllauthTwoFactorMiddleware',
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

.. warning::

    Any login view that is *not* provided by django-allauth will bypass the
    allauth workflow (including two-factor authentication). The Django admin
    site includes an additional login view (usually available at
    ``/admin/login``).

    The easiest way to fix this is to wrap it in ``staff_member_required`` decorator
    and disallow access to the admin site to all, except logged in staff members 
    through allauth workflow.
    (the code only works if you use the standard admin site, if you have a
    custom admin site you'll need to customize this more):

    .. code-block:: python

        from django.contrib import admin
        from django.contrib.admin.views.decorators import staff_member_required

        # Ensure users go through the allauth workflow when logging into admin.
        admin.site.login = staff_member_required(admin.site.login, login_url='/accounts/login')
        # Run the standard admin set-up.
        admin.autodiscover()
