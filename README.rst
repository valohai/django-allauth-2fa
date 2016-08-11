django-allauth-2fa
==================

Adds two factor authentication to django-allauth.


Installation
------------

Install `django-allauth-2fa` with pip::

    pip install django-allauth-2fa


Adjust your settings accordingly:

.. code-block:: python

    INSTALLED_APPS = (
        # Install allauth as normal.
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        # Install the Django OTP package along with the TOTP and recovery codes
        # packages.
        'django_otp',
        'django_otp.plugins.otp_totp',
        'django_otp.plugins.otp_static',
        # Finally, install allauth 2FA.
        'allauth_2fa',
    )

    MIDDLEWARE_CLASSES = (
        # ...
        'django_otp.middleware.OTPMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
    )

    # Set the allauth adapter to be the 2FA adapter.
    ACCOUNT_ADAPTER = 'allauth_2fa.adapter.OTPAdapter'

    SITE_ID = 1


Remember to migrate and set the domain and display name for your site!
