from allauth.account import app_settings
from django.conf import settings

TEMPLATE_EXTENSION = getattr(settings, 'ALLAUTH_2FA_TEMPLATE_EXTENSION', app_settings.TEMPLATE_EXTENSION)
BACKUP_DEVICE_NAME = getattr(settings, 'ALLAUTH_2FA_BACKUP_DEVICE_NAME', 'backup')
