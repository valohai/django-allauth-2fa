from __future__ import annotations

from base64 import b64encode

from allauth.account.adapter import get_adapter
from allauth.utils import get_form_class
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.views.generic import FormView
from django.views.generic import TemplateView
from django_otp.plugins.otp_static.models import StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice

from allauth_2fa import app_settings
from allauth_2fa.forms import TOTPAuthenticateForm
from allauth_2fa.forms import TOTPDeviceForm
from allauth_2fa.forms import TOTPDeviceRemoveForm
from allauth_2fa.mixins import ValidTOTPDeviceRequiredMixin
from allauth_2fa.utils import generate_totp_config_svg
from allauth_2fa.utils import get_device_base32_secret
from allauth_2fa.utils import user_has_valid_totp_device


class TwoFactorAuthenticate(FormView):
    template_name = f"allauth_2fa/authenticate.{app_settings.TEMPLATE_EXTENSION}"
    form_class = TOTPAuthenticateForm

    def dispatch(self, request, *args, **kwargs):
        # If the user is not about to enter their two-factor credentials,
        # redirect to the login page (they shouldn't be here!). This includes
        # anonymous users.
        if "allauth_2fa_user_id" not in request.session:
            # Don't use the redirect_to_login here since we don't actually want
            # to include the next parameter.
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "authenticate", self.form_class)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.session["allauth_2fa_user_id"]
        kwargs["user"] = get_user_model().objects.get(id=user_id)
        return kwargs

    def form_valid(self, form):
        """
        The allauth 2fa login flow is now done (the user logged in successfully
        with 2FA), continue the logic from allauth.account.utils.perform_login
        since it was interrupted earlier.

        """
        adapter = get_adapter(self.request)
        # 2fa kicked in at `pre_login()`, so we need to continue from there.
        login_kwargs = adapter.unstash_pending_login_kwargs(self.request)
        adapter.login(self.request, form.user)
        return adapter.post_login(self.request, form.user, **login_kwargs)


class TwoFactorSetup(LoginRequiredMixin, FormView):
    template_name = f"allauth_2fa/setup.{app_settings.TEMPLATE_EXTENSION}"
    form_class = TOTPDeviceForm
    success_url = reverse_lazy(app_settings.SETUP_SUCCESS_URL)

    def dispatch(self, request, *args, **kwargs):
        # If the user has 2FA setup already, redirect them to the backup tokens.
        if user_has_valid_totp_device(request.user):
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def _new_device(self):
        """
        Replace any unconfirmed TOTPDevices with a new one for confirmation.

        This needs to be done whenever a GET request to the page is received OR
        if the confirmation of the device fails.
        """
        self.request.user.totpdevice_set.filter(confirmed=False).delete()
        self.device = TOTPDevice.objects.create(user=self.request.user, confirmed=False)

    def get(self, request, *args, **kwargs):
        # Whenever this page is loaded, create a new device (this ensures a
        # user's QR code isn't shown multiple times).
        self._new_device()
        return super().get(request, *args, **kwargs)

    def get_qr_code_kwargs(self) -> dict[str, str]:
        """
        Get the configuration for generating a QR code.

        The fields required are:
        - `label`: identifies which account a key is associated with. Contains an
            account name, preferably prefixed by an issuer name and a colon, e.g.
            `issuer: account`.
        - `issuer`: indicates the provider or service this account is associated with.
        """

        issuer = get_current_site(self.request).name

        return {
            "issuer": issuer,
            "label": f"{issuer}: {self.request.user.get_username()}",
        }

    def get_qr_code_data_uri(self):
        svg_data = generate_totp_config_svg(
            device=self.device,
            **self.get_qr_code_kwargs(),
        )
        return f"data:image/svg+xml;base64,{force_str(b64encode(svg_data))}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qr_code_url"] = self.get_qr_code_data_uri()
        context["secret"] = get_device_base32_secret(self.device)
        return context

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "setup", self.form_class)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Confirm the device.
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the confirmation code was wrong, generate a new device.
        self._new_device()
        return super().form_invalid(form)


class TwoFactorRemove(ValidTOTPDeviceRequiredMixin, FormView):
    template_name = f"allauth_2fa/remove.{app_settings.TEMPLATE_EXTENSION}"
    form_class = TOTPDeviceRemoveForm
    success_url = reverse_lazy(app_settings.REMOVE_SUCCESS_URL)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "remove", self.form_class)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TwoFactorBackupTokens(ValidTOTPDeviceRequiredMixin, TemplateView):
    template_name = f"allauth_2fa/backup_tokens.{app_settings.TEMPLATE_EXTENSION}"
    # This can be overridden in a subclass to True,
    # to have that particular view always reveal the tokens.
    reveal_tokens = bool(app_settings.ALWAYS_REVEAL_BACKUP_TOKENS)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        static_device, _ = self.request.user.staticdevice_set.get_or_create(
            name="backup",
        )

        if static_device:
            context["backup_tokens"] = static_device.token_set.all()
            context["reveal_tokens"] = self.reveal_tokens

        return context

    def post(self, request, *args, **kwargs):
        static_device, _ = request.user.staticdevice_set.get_or_create(name="backup")
        static_device.token_set.all().delete()
        for _ in range(app_settings.BACKUP_TOKENS_NUMBER):
            static_device.token_set.create(token=StaticToken.random_token())
        self.reveal_tokens = True
        return self.get(request, *args, **kwargs)
