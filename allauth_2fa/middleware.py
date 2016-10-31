from django.core.urlresolvers import resolve
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class AllauthTwoFactorMiddleware(MiddlewareMixin):
    """
    Reset the login flow if another page is loaded halfway through the login.
    (I.e. if the user has logged in with a username/password, but not yet
    entered their two-factor credentials.) This makes sure a user does not stay
    half logged in by mistake.

    """

    def process_request(self, request):
        match = resolve(request.path)
        if not match.url_name or not match.url_name.startswith(
                'two-factor-authenticate'):
            try:
                del request.session['allauth_2fa_user_id']
            except KeyError:
                pass
