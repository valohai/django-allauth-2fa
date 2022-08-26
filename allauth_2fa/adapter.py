from urllib.parse import urlencode

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import get_next_redirect_url
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from allauth_2fa.utils import user_has_valid_totp_device


class OTPAdapter(DefaultAccountAdapter):
    def has_2fa_enabled(self, user):
        """Returns True if the user has 2FA configured."""
        return user_has_valid_totp_device(user)

    def pre_login(self, request, user, **kwargs):
        response = super().pre_login(request, user, **kwargs)
        if response:
            return response

        # Require two-factor authentication if it has been configured.
        if self.has_2fa_enabled(user):
            self.stash_pending_login(request, user, **kwargs)
            redirect_url = reverse("two-factor-authenticate")
            query_params = request.GET.copy()
            next_url = get_next_redirect_url(request)
            if next_url:
                query_params["next"] = next_url
            if query_params:
                redirect_url += "?" + urlencode(query_params)

            raise ImmediateHttpResponse(response=HttpResponseRedirect(redirect_url))

    def stash_pending_login(self, request, user, **kwargs):
        # Cast to string for the case when this is not a JSON serializable
        # object, e.g. a UUID.
        request.session["allauth_2fa_user_id"] = str(user.id)
        login_kwargs = kwargs.copy()
        signal_kwargs = login_kwargs.get("signal_kwargs")
        if signal_kwargs:
            sociallogin = signal_kwargs.get("sociallogin")
            if sociallogin:
                signal_kwargs = signal_kwargs.copy()
                signal_kwargs["sociallogin"] = sociallogin.serialize()
                login_kwargs["signal_kwargs"] = signal_kwargs
        request.session["allauth_2fa_login"] = login_kwargs

    def unstash_pending_login_kwargs(self, request):
        login_kwargs = request.session.pop("allauth_2fa_login", None)
        if login_kwargs is None:
            raise PermissionDenied()
        signal_kwargs = login_kwargs.get("signal_kwargs")
        if signal_kwargs:
            sociallogin = signal_kwargs.get("sociallogin")
            if sociallogin:
                signal_kwargs["sociallogin"] = SocialLogin.deserialize(sociallogin)
        return login_kwargs