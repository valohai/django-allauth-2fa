.. :changelog:

Changelog
#########

next
====

* Improves documentation for protection Django admin with 2FA. Contributed by
  @hailkomputer in #91.
* Autocomplete on the token entry form is disabled. Contributed by @qvicksilver
  in #95.

0.8 February 3, 2020
====================

* Drop support for Python 2.7 and Python 3.4.
* Officially support Python 3.7 and 3.8.
* Drop support for Django 2.0 and Django 2.1.
* Officially support Django 3.0.

0.7 September 10, 2019
======================

* Remove more code that was for Django < 1.11.
* Officially support Django 2.0 and Django 2.1.
* Officially support django-otp 0.7.
* Do not include test code in distribution, fix from @akx, PR #67.
* Support for more complex user IDs (e.g. UUIDs), fix from @chromakey, see issue
  #64 / PR #66.
* The extension used by the 2FA templates is customizable. Originally in PR #69
  by @akx, split into PR #71.
* The QR code is now included inline as an SVG instead of being a separate view.
  PR #74 by @akx.
* A new mixin is included to enforce a user having 2FA enabled for particular
  views. Added in PR #73 by @akx.
* Passing additional context to the ``TwoFactorBackupTokens`` was broken. This
  was fixed in PR #73 by @akx.
* A configuration option (``ALLAUTH_2FA_ALWAYS_REVEAL_BACKUP_TOKENS``) was added
  to only show the static tokens once (during creation)> PR #75 by @akx.

0.6 February 13, 2018
=====================

* Drop support for Django < 1.11, these are no longer supported by
  django-allauth (as of 0.35.0).

0.5 December 21, 2017
=====================

* Avoid an exception if a user without any configured devices tries to view a QR
  code. This view now properly 404s.
* Redirect users to configure 2FA is they attempt to configure backup tokens
  without enabling 2FA first.
* Add base middleware to ensure particular users (e.g. superusers) have 2FA
  enabled.
* Drop official support for Django 1.9 and 1.10, they're
  `no longer supported <https://www.djangoproject.com/download/#supported-versions>`_
  by the Django project.
* Added Sphinx-generated documentation. A rendered version
  `is available at <https://django-allauth-2fa.readthedocs.io/>`_.

0.4.4 March 24, 2017
====================

* Adds trailing slashes to the URL patterns. This is backwards compatible with
  the old URLs.
* Properly support installing in Python 3 via PyPI.

0.4.3 January 18, 2017
======================

* Adds support for forwarding ``GET`` parameters through the 2FA workflow. This
  fixes ``next`` not working when logging in using 2FA.

0.4.2 December 15, 2016
=======================

* Reverts the fix in 0.4.1 as this breaks custom adapters that inherit from
  ``OTPAdapter`` and *don't* override the ``login`` method.

0.4.1 December 14, 2016
=======================

* Fixed a bug when using a custom adapter that doesn't inherit from
  ``OTPAdapter`` and that overrides the ``login`` method.

0.4 November 7, 2016
====================

* Properly continue the allauth login workflow after successful 2FA login, e.g.
  send allauth signals
* Support using ``MIDDLEWARE`` setting with Django 1.10.
* Support customer ``USERNAME_FIELD`` on the auth model.

0.3.2 October 26, 2016
======================

* Fix an error when hitting the TwoFactorBackupTokens view as a non-anonymous
  user.

0.3.1 October 5, 2016
=====================

* Properly handle an ``AnonymousUser`` hitting the views.

0.3 October 5, 2016
===================

* Support custom ``User`` models.
* Fixed a bug where a user could end up half logged in if they didn't complete
  the two-factor login flow. A user's login flow will now be reset. Requires
  enabled the included middle: ``allauth_2fa.middleware.AllauthTwoFactorMiddleware``.
* Disable autocomplete on the two-factor code input form.
* Properly redirect anonymous users.
* Minor simplifications of code (and inherit more code from django-otp).
* Minor updates to documentation.

0.2 September 9, 2016
=====================

* Add tests / tox / Travis support.
* Don't pin dependencies.
* Officially support Django 1.10, drop support for Django 1.7.

0.1.4 May 2, 2016
=================

* Autofocus the token input field on forms.

0.1.3 January 20, 2016
======================

* Fix deprecation notices for Django 1.10.

0.1.2 November 23, 2015
=======================

* Fixed an error when a user enters invalid input into the token form.

0.1.1 October 21, 2015
======================

* Project reorganization and clean-up.
* Added support for Microsoft Authenticator.
* Support being installed via pip.
* Pull more configuration from Django settings (success URL).
* Support disabling two-factor for an account.

0.1 April 4, 2015
=================

* Initial version by Víðir Valberg Guðmundsson
