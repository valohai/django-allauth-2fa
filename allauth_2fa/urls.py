from django.urls import path

from allauth_2fa import views

urlpatterns = [
    path("two-factor-authenticate/",
        views.TwoFactorAuthenticate.as_view(),
        name="two-factor-authenticate"),

    path("two_factor/setup/",
        views.TwoFactorSetup.as_view(),
        name="two-factor-setup"),

    path("two_factor/backup_tokens/",
        views.TwoFactorBackupTokens.as_view(),
        name="two-factor-backup-tokens"),

    path("two_factor/remove/",
        views.TwoFactorRemove.as_view(),
        name="two-factor-remove"),
]
