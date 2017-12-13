Advanced Configuration
----------------------

Forcing a User to Use 2FA
'''''''''''''''''''''''''

A ``User`` can be forced to use 2FA based on any requirements (e.g. superusers
or being in a particular group). This is implemented by subclassing the
``allauth_2fa.middleware.BaseRequire2FAMiddleware`` and implementing the
``require_2fa`` method on it. This middleware needs to be added to your
``MIDDLEWARE_CLASSES`` setting.

For example, to require a user to be a superuser:

.. code-block:: python

    from allauth_2fa.middleware import BaseRequire2FAMiddleware

    class RequireSuperuser2FAMiddleware(BaseRequire2FAMiddleware):
        def require_2fa(self, request):
            # Superusers are require to have 2FA.
            return request.user.is_superuser

If the user doesn't have 2FA enabled they will be redirected to the 2FA
configuration page and will not be allowed to access (most) other pages.
