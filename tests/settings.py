import django

SECRET_KEY = 'not_empty'
SITE_ID = 1
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.urls'
LOGIN_REDIRECT_URL = '/accounts/password/change/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

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
    # Required to render the default template for 'account_login'.
    'allauth.socialaccount',

    # Configure the django-otp package.
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',

    # Enable two-factor auth.
    'allauth_2fa',

    # Test app.
    'tests',
)

MIDDLEWARE = (
    # Configure Django auth package.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Configure the django-otp package.
    'django_otp.middleware.OTPMiddleware',

    # Reset login flow middleware.
    'allauth_2fa.middleware.AllauthTwoFactorMiddleware',
)

if django.VERSION < (2,):
    MIDDLEWARE += ('django.contrib.auth.middleware.SessionAuthenticationMiddleware',)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Enable two-factor auth.
ACCOUNT_ADAPTER = 'allauth_2fa.adapter.OTPAdapter'
