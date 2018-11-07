Configuration
=============

``ALLAUTH_2FA_TEMPLATE_EXTENSION``
----------------------------------

ALlows you to override the extension for the templates used by the internal
views of django-allauth-2fa.

Defaults to ``ACCOUNT_TEMPLATE_EXTENSION`` from allauth, which is ``html`` by
default.

This can be used to allow a different template engine for 2FA views.

``ALLAUTH_2FA_BACKUP_DEVICE_NAME``
----------------------------------

Set the name for the static backup code OTP device.

Defaults to ``backup``.


``ALLAUTH_2FA_BACKUP_TOKEN_COUNT``
----------------------------------

The number of backup tokens to create in the built-in backup
code view.

Defaults to 3.
