.. :changelog:

Changelog
#########

0.12.0 - January 2025
=====================

Note
----

This may be the last version of django-allauth-2fa under this stewardship;
allauth contains its own ``allauth.mfa`` package that should be used instead
for versions of Allauth >= 0.58.0.  The dependency range for ``allauth`` in this
version has been updated accordingly; this release will conflict with newer versions
of ``allauth`` on purpose.

See https://github.com/valohai/django-allauth-2fa/issues/189 for discussion.

You can use the experimental ``allauth_2fa_migrate`` management command to create
``allauth.mfa`` Authenticator objects from your ``allauth_2fa`` data before switching
your production environment over to ``allauth.mfa``.

Possibly breaking changes
-------------------------

* You can't write to `allauth_2fa.app_settings` variables anymore;
  instead modify the underlying `django.conf.settings` settings.

New features and fixes
----------------------

* Add flag to make the required entry of an OTP code for device removal optional (#169)
* Add setting to allow generating a different number of backup tokens (#192)
* Potential bugfix for ``redirect_field_name`` AttributeError (#196)

0.11.1 - July 13, 2023
======================

Patch release to address a packaging issue where templates weren't included (#176, #177).

0.11.0 - July 4, 2023
=====================

We didn't wait one year from the last release for this on purpose, I swear!

Minimum dependency versions
---------------------------

* The minimum version of Python for this release is 3.7.
* The minimum version of Django for this release is 3.2.
* The minimum version of django-otp for this release is 1.1.x.
* The minimum version of django-allauth for this release is 0.53.0.

Possibly breaking changes
-------------------------

* The `token` field in forms is now `otp_token`; if you have subclassed forms,
  or are using custom templates, this may require adjustment.

New features
------------

* Allow customizing view success URLs via app_settings
* Show secret on setup page to allow for non-QR-code devices
* You can customize the QR code generation arguments in TwoFactorSetup (#156)
* 2FA can be disabled using backup tokens (#155)
* You can now override the forms used by the views using settings, like allauth does (#161)

Infrastructure
--------------

* The package now has (partial) type annotations.

0.10.0 - July 4, 2022
=====================

If you're using a custom template for the 2FA token removal view,
note that you will need to also display the ``token`` field beginning
with this version (PR #135 in particular).

The minimum version of django-otp was bumped to 0.6.x.

* Update CI bits and bobs by @akx in #137
* Drop support for django-otp 0.5.x by @akx in #138
* Require user token to disable 2FA by @SchrodingersGat in #135

0.9 - April 11, 2022
====================

This release dropped support for Python 3.5 and added support for Django 4.0.

* Improves documentation for protection Django admin with 2FA. Contributed by @hailkomputer in #91.
* Autocomplete on the token entry form is disabled. Contributed by @qvicksilver in #95.
* Stop restricting a class of an adapter in `TwoFactorAuthenticate` by @illia-v in #96
* Use same base template as upstream allauth by @ErwinJunge in #98
* Redirect to next, when given via GET or POST by @ErwinJunge in #99
* Allow TOTP removal when no backup device is present by @akx in #126
* Fix for subclassed OTP adapter by @squio in #129
* Replace Travis with GitHub Actions by @akx in #110
* Drop EOL Python 3.5, modernize for 3.6+ by @akx in #106
* Remove Django 1.11 from tox, and add Django 4.0b1. by @valberg in #118
* Typo in docs by @beckedorf in #122
* Add pre-commit, and run it. by @valberg in #121
* Rename master -> main by @akx in #123
* Declarative setup.cfg by @akx in #124
* Use Py.test for tests + fix coverage reporting by @akx in #127
* Require2FAMiddleware improvements by @akx in #107
* Miscellaneous housekeeping by @akx in #130

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
