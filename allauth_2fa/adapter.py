from __future__ import annotations

from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.models import SocialLogin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from allauth_2fa.utils import get_next_query_string
from allauth_2fa.utils import user_has_valid_totp_device


class OTPAdapter(DefaultAccountAdapter):
    def has_2fa_enabled(self, user) -> bool:
        """Returns True if the user has 2FA configured."""
        return user_has_valid_totp_device(user)

    def pre_login(
        self,
        request: HttpRequest,
        user,
        **kwargs,
    ) -> HttpResponse | None:
        response = super().pre_login(request, user, **kwargs)
        if response:
            return response

        # Require two-factor authentication if it has been configured.
        if self.has_2fa_enabled(user):
            self.stash_pending_login(request, user, kwargs)
            redirect_url = self.get_2fa_authenticate_url(request)
            raise ImmediateHttpResponse(response=HttpResponseRedirect(redirect_url))

        # Otherwise defer to the original allauth adapter.
        return super().login(request, user)

    def get_2fa_authenticate_url(self, request: HttpRequest) -> str:
        """
        Get the URL to redirect to for finishing 2FA authentication.
        """
        redirect_url = reverse("two-factor-authenticate")

        # Add "next" parameter to the URL if possible.
        query_string = get_next_query_string(request)
        if query_string:
            redirect_url += query_string

        return redirect_url

    def stash_pending_login(
        self,
        request: HttpRequest,
        user,
        login_kwargs: dict,
    ) -> None:
        """Here, we're going to stash the pending login so that it can be
        resumed at a later point. The `login_kwargs` contain meta information on
        the login which we need to store.

        The `login_kwargs` passed is a dictionary, and we're going to store that
        in the session. While doing so, we need to mutate it a bit to ensure
        serializability.  Mutating a dictionary passed to us is not something
        the caller expects, so we're going to make a shallow copy to prevent the
        caller from being impacted. Shallow is fine, as we're only setting new
        keys and not altering existing values.
        """
        # Cast to string for the case when this is not a JSON serializable
        # object, e.g. a UUID.
        request.session["allauth_2fa_user_id"] = str(user.id)
        login_kwargs = login_kwargs.copy()
        signal_kwargs = login_kwargs.get("signal_kwargs")
        if signal_kwargs:
            sociallogin = signal_kwargs.get("sociallogin")
            if sociallogin:
                signal_kwargs = signal_kwargs.copy()
                signal_kwargs["sociallogin"] = sociallogin.serialize()
                login_kwargs["signal_kwargs"] = signal_kwargs
        request.session["allauth_2fa_login"] = login_kwargs

    def unstash_pending_login_kwargs(self, request: HttpRequest) -> dict:
        login_kwargs = request.session.pop("allauth_2fa_login", None)
        if login_kwargs is None:
            raise PermissionDenied()
        signal_kwargs = login_kwargs.get("signal_kwargs")
        if signal_kwargs:
            sociallogin = signal_kwargs.get("sociallogin")
            if sociallogin:
                signal_kwargs["sociallogin"] = SocialLogin.deserialize(sociallogin)
        return login_kwargs
