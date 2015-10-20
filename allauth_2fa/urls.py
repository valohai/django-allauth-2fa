from django.conf.urls import url, patterns

from . import views


urls =  [
    url(r"^two-factor-authenticate$",
        views.two_factor_authenticate,
        name="two-factor-authenticate"),

    url(r"^two_factor/setup$",
        views.two_factor_setup,
        name="two-factor-setup"),

    url(r"^two_factor/backup_tokens$",
        views.two_factor_backup_tokens,
        name="two-factor-backup-tokens"),

    url(r"^two_factor/qr_code$",
        views.two_factor_qr_code_generator,
        name="two-factor-qr-code"),
]

urlpatterns = patterns('', *urls)
