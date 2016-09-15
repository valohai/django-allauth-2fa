from django.core.urlresolvers import resolve


class AllauthTwoFactorMiddleware(object):
    """Resets the login flow when another page is loaded halfway through."""

    def process_request(self, request):
        if resolve(request.path).url_name != 'two-factor-authenticate':
            try:
                del request.session['user_id']
            except KeyError:
                pass
