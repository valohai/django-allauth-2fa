from allauth.exceptions import ImmediateHttpResponse

from allauth.account.adapter import DefaultAccountAdapter
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class OTPAdapterMixin:
    def login(self, request, user):
        if user.totpdevice_set.all():
            request.session['user_id'] = user.id
            raise ImmediateHttpResponse(
                response=HttpResponseRedirect(
                    reverse('two-factor-authenticate')
                )
            )
        return super(OTPAdapterMixin, self).login(request, user)


class OTPAdapter(OTPAdapterMixin, DefaultAccountAdapter):
    pass
