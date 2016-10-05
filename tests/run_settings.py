"""The same as tests.settings, but appropriate to actually run with runserver, etc."""

from tests.settings import *


DEBUG = True
DATABASES['default']['NAME'] = 'db.sqlite'

INSTALLED_APPS += ('django_extensions', )
