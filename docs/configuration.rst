Configuration
=============

``ALLAUTH_2FA_TEMPLATE_EXTENSION``
----------------------------------

ALlows you to override the extension for the templates used by the internal
views of django-allauth-2fa.

Defaults to ``ACCOUNT_TEMPLATE_EXTENSION`` from allauth, which is ``html`` by
default.

This can be used to allow a different template engine for 2FA views.

``ALLAUTH_2FA_ALWAYS_REVEAL_BACKUP_TOKENS``
-------------------------------------------

Whether to always show the remaining backup tokens on the
Backup Tokens view, or only when they're freshly generated.

Defaults to ``True``.
