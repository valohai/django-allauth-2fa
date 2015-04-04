# django-allauth-2fa

Adds two factor authentication to django-allauth.


## Installation

Install `django-allauth-2fa` with pip:

    pip install django-allauth-2fa


Adjust your settings accordingly:

    INSTALLED_APPS = (
        # ...
        'django_otp',
        'django_otp.plugins.otp_totp',
        'django_otp.plugins.otp_hotp',
        'django_otp.plugins.otp_static',
        'allauth',
        'allauth.account',
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

    ACCOUNT_ADAPTER = 'allauth_2fa.adapter.OTPAdapter'


Remember to migrate!
