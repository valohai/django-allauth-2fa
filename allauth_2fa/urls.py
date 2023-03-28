from __future__ import annotations

from django.urls import path

from allauth_2fa import views

urlpatterns = [
    path(
        "authenticate/",
        views.TwoFactorAuthenticate.as_view(),
        name="two-factor-authenticate",
    ),
    path(
        "setup/",
        views.TwoFactorSetup.as_view(),
        name="two-factor-setup",
    ),
    path(
        "backup-tokens/",
        views.TwoFactorBackupTokens.as_view(),
        name="two-factor-backup-tokens",
    ),
    path(
        "remove/",
        views.TwoFactorRemove.as_view(),
        name="two-factor-remove",
    ),
]
