from allauth.account import app_settings as allauth_settings

from django.conf import settings

TEMPLATE_EXTENSION = getattr(settings,
                             'ALLAUTH_2FA_TEMPLATE_EXTENSION',
                             allauth_settings.TEMPLATE_EXTENSION)

BACKUP_DEVICE_NAME = getattr(settings, 'ALLAUTH_2FA_BACKUP_DEVICE_NAME', 'backup')

BACKUP_TOKEN_COUNT = int(getattr(settings, 'ALLAUTH_2FA_BACKUP_TOKEN_COUNT', 3))
