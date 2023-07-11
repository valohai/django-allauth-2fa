from __future__ import annotations

import contextlib

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django_otp.forms import OTPAuthenticationFormMixin
from django_otp.plugins.otp_totp.models import TOTPDevice

from allauth_2fa import app_settings

DEFAULT_TOKEN_WIDGET_ATTRS = {
    "autofocus": "autofocus",
    "autocomplete": "off",
    "inputmode": "numeric",
}


class _TokenToOTPTokenMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if "token" in self.fields or "token" in self.data:
            self._raise_token_exception()

    @property
    def token(self):
        self._raise_token_exception()

    def _raise_token_exception(self):
        raise ImproperlyConfigured(
            f"The field `token` in {self} has been renamed to `otp_token`.",
        )


class TOTPAuthenticateForm(OTPAuthenticationFormMixin, forms.Form):
    otp_token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.fields["otp_token"].widget.attrs.update(DEFAULT_TOKEN_WIDGET_ATTRS)
        self.user = user

    def clean(self) -> dict:
        self.clean_otp(self.user)
        return self.cleaned_data


class TOTPDeviceForm(_TokenToOTPTokenMixin, forms.Form):
    otp_token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, metadata=None, **kwargs):
        super().__init__(**kwargs)
        self.fields["otp_token"].widget.attrs.update(DEFAULT_TOKEN_WIDGET_ATTRS)
        self.user = user
        self.metadata = metadata or {}

    def clean_otp_token(self):
        token = self.cleaned_data.get("otp_token")

        # Find the unconfirmed device and attempt to verify the token.
        self.device = self.user.totpdevice_set.filter(confirmed=False).first()
        if not self.device.verify_token(token):
            raise forms.ValidationError(_("The entered token is not valid"))

        return token

    def save(self) -> TOTPDevice:
        # The device was found to be valid, delete other confirmed devices and
        # confirm the new device.
        self.user.totpdevice_set.filter(confirmed=True).delete()
        self.device.confirmed = True
        self.device.save()

        return self.device


class TOTPDeviceRemoveForm(
    _TokenToOTPTokenMixin,
    OTPAuthenticationFormMixin,
    forms.Form,
):
    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)

        self.user = user
        # user has to enter OTP token to remove device
        # if REQUIRE_OTP_ON_DEVICE_REMOVAL is True
        if app_settings.REQUIRE_OTP_ON_DEVICE_REMOVAL:
            self.fields["otp_token"] = forms.CharField(label=_("Token"), required=True)
            self.fields["otp_token"].widget.attrs.update(DEFAULT_TOKEN_WIDGET_ATTRS)

    def clean(self):
        # clean OTP token if REQUIRE_OTP_ON_DEVICE_REMOVAL is True
        if app_settings.REQUIRE_OTP_ON_DEVICE_REMOVAL:
            self.clean_otp(self.user)
        return self.cleaned_data

    def save(self) -> None:
        with contextlib.suppress(ObjectDoesNotExist):
            # Delete any backup tokens and their related static device.
            static_device = self.user.staticdevice_set.get(name="backup")
            static_device.token_set.all().delete()
            static_device.delete()

        # Delete TOTP device.
        device = TOTPDevice.objects.get(user=self.user)
        device.delete()
