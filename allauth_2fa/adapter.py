try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from allauth.exceptions import ImmediateHttpResponse
from allauth.account.adapter import DefaultAccountAdapter


class OTPAdapter(DefaultAccountAdapter):

    def login(self, request, user):

        # Require two-factor authentication if it has been configured.
        if user.totpdevice_set.filter(confirmed=True).all():
            request.session['allauth_2fa_user_id'] = user.id

            redirect_url = reverse('two-factor-authenticate')
            # Add GET parameters to the URL if they exist.
            if request.GET:
                redirect_url += u'?' + urlencode(request.GET)

            raise ImmediateHttpResponse(
                response=HttpResponseRedirect(redirect_url)
            )

        # Otherwise defer to the original allauth adapter.
        return super(OTPAdapter, self).login(request, user)
