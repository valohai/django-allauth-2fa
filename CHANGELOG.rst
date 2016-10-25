.. :changelog:

Changelog
#########

0.4 xxx xx, 2016
================

* Properly continue the allauth login workflow after successful 2FA login, e.g.
  send allauth signals
* Support using ``MIDDLEWARE`` setting with Django 1.10.

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
