try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse

from django.http import HttpResponseRedirect
from django.urls import reverse


class OTPAdapter(DefaultAccountAdapter):
    def has_2fa_enabled(self, user):
        """Returns True if the user has 2FA configured."""
        return user.totpdevice_set.filter(confirmed=True).exists()

    def login(self, request, user):
        # Require two-factor authentication if it has been configured.
        if self.has_2fa_enabled(user):
            request.session['allauth_2fa_user_id'] = str(user.id)

            redirect_url = reverse('two-factor-authenticate')
            # Add GET parameters to the URL if they exist.
            if request.GET:
                redirect_url += u'?' + urlencode(request.GET)

            raise ImmediateHttpResponse(
                response=HttpResponseRedirect(redirect_url)
            )

        # Otherwise defer to the original allauth adapter.
        return super(OTPAdapter, self).login(request, user)
