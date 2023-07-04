from __future__ import annotations

from allauth.account import app_settings as allauth_settings
from django.conf import settings

TEMPLATE_EXTENSION = getattr(
    settings,
    "ALLAUTH_2FA_TEMPLATE_EXTENSION",
    allauth_settings.TEMPLATE_EXTENSION,
)

ALWAYS_REVEAL_BACKUP_TOKENS = bool(
    getattr(settings, "ALLAUTH_2FA_ALWAYS_REVEAL_BACKUP_TOKENS", True),
)

REMOVE_SUCCESS_URL = getattr(
    settings,
    "ALLAUTH_2FA_REMOVE_SUCCESS_URL",
    "two-factor-setup",
)

SETUP_SUCCESS_URL = getattr(
    settings,
    "ALLAUTH_2FA_SETUP_SUCCESS_URL",
    "two-factor-backup-tokens",
)

FORMS = getattr(settings, "ALLAUTH_2FA_FORMS", {})
