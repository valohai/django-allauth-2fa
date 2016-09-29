from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from allauth.exceptions import ImmediateHttpResponse
from allauth.account.adapter import DefaultAccountAdapter


class OTPAdapter(DefaultAccountAdapter):

    def login(self, request, user):

        # Require two-factor authentication if it has been configured.
        if user.totpdevice_set.filter(confirmed=True).all():
            request.session['allauth_2fa_user_id'] = user.id
            raise ImmediateHttpResponse(
                response=HttpResponseRedirect(
                    reverse('two-factor-authenticate')
                )
            )

        # Otherwise defer to the original allauth adapter.
        return super(OTPAdapter, self).login(request, user)
