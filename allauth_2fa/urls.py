from django.conf.urls import url

from allauth_2fa import views

urlpatterns = [
    url(r"^two-factor-authenticate/?$",
        views.TwoFactorAuthenticate.as_view(),
        name="two-factor-authenticate"),

    url(r"^two_factor/setup/?$",
        views.TwoFactorSetup.as_view(),
        name="two-factor-setup"),

    url(r"^two_factor/backup_tokens/?$",
        views.TwoFactorBackupTokens.as_view(),
        name="two-factor-backup-tokens"),

    url(r"^two_factor/remove/?$",
        views.TwoFactorRemove.as_view(),
        name="two-factor-remove"),
]
