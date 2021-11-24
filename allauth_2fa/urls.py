from django.urls import re_path

from allauth_2fa import views

urlpatterns = [
    re_path(
        r"^two-factor-authenticate/?$",
        views.TwoFactorAuthenticate.as_view(),
        name="two-factor-authenticate",
    ),
    re_path(
        r"^two_factor/setup/?$",
        views.TwoFactorSetup.as_view(),
        name="two-factor-setup",
    ),
    re_path(
        r"^two_factor/backup_tokens/?$",
        views.TwoFactorBackupTokens.as_view(),
        name="two-factor-backup-tokens",
    ),
    re_path(
        r"^two_factor/remove/?$",
        views.TwoFactorRemove.as_view(),
        name="two-factor-remove",
    ),
]
