from urllib.parse import urlencode

from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from allauth_2fa.utils import user_has_valid_totp_device


class OTPAdapter(DefaultAccountAdapter):
    def has_2fa_enabled(self, user):
        """Returns True if the user has 2FA configured."""
        return user_has_valid_totp_device(user)

    def login(self, request, user):
        # Require two-factor authentication if it has been configured.
        if self.has_2fa_enabled(user):
            # Cast to string for the case when this is not a JSON serializable
            # object, e.g. a UUID.
            request.session["allauth_2fa_user_id"] = str(user.id)
            redirect_url = self.get_2fa_authenticate_url(request)
            raise ImmediateHttpResponse(response=HttpResponseRedirect(redirect_url))

        # Otherwise defer to the original allauth adapter.
        return super().login(request, user)

    def get_2fa_authenticate_url(self, request):
        """
        Get the URL to redirect to for finishing 2FA authentication.
        """
        redirect_url = reverse("two-factor-authenticate")

        # Add "next" parameter to the URL if possible.
        # If the view function smells like a class-based view, we can interrogate it.
        if getattr(request.resolver_match.func, "view_class", None):
            view = request.resolver_match.func.view_class()
            view.request = request
            success_url = view.get_success_url()
            query_params = request.GET.copy()
            if success_url:
                query_params[view.redirect_field_name] = success_url
            if query_params:
                redirect_url += "?" + urlencode(query_params)

        return redirect_url
