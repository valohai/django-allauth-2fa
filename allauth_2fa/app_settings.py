from __future__ import annotations

from allauth.account import app_settings as allauth_settings
from django.conf import settings


class _AppSettings:
    @property
    def TEMPLATE_EXTENSION(self) -> str:
        return getattr(
            settings,
            "ALLAUTH_2FA_TEMPLATE_EXTENSION",
            allauth_settings.TEMPLATE_EXTENSION,
        )

    @property
    def ALWAYS_REVEAL_BACKUP_TOKENS(self) -> bool:
        return bool(getattr(settings, "ALLAUTH_2FA_ALWAYS_REVEAL_BACKUP_TOKENS", True))

    @property
    def REMOVE_SUCCESS_URL(self) -> str:
        return getattr(
            settings,
            "ALLAUTH_2FA_REMOVE_SUCCESS_URL",
            "two-factor-setup",
        )

    @property
    def SETUP_SUCCESS_URL(self) -> str:
        return getattr(
            settings,
            "ALLAUTH_2FA_SETUP_SUCCESS_URL",
            "two-factor-backup-tokens",
        )

    @property
    def FORMS(self) -> dict:
        return getattr(settings, "ALLAUTH_2FA_FORMS", {})

    @property
    def REQUIRE_OTP_ON_DEVICE_REMOVAL(self) -> bool:
        return getattr(
            settings,
            "ALLAUTH_2FA_REQUIRE_OTP_ON_DEVICE_REMOVAL",
            True,
        )

    @property
    def BACKUP_TOKENS_NUMBER(self) -> int:
        return getattr(
            settings,
            "ALLAUTH_2FA_BACKUP_TOKENS_NUMBER",
            3,
        )


_app_settings = _AppSettings()


def __getattr__(name: str):
    # See https://peps.python.org/pep-0562/ :)
    return getattr(_app_settings, name)
