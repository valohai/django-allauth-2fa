import contextlib

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django_otp.forms import OTPAuthenticationFormMixin
from django_otp.plugins.otp_totp.models import TOTPDevice

DEFAULT_TOKEN_WIDGET_ATTRS = {
    "autofocus": "autofocus",
    "autocomplete": "off",
    "inputmode": "numeric",
}


class TOTPAuthenticateForm(OTPAuthenticationFormMixin, forms.Form):
    otp_token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.fields["otp_token"].widget.attrs.update(DEFAULT_TOKEN_WIDGET_ATTRS)
        self.user = user

    def clean(self):
        self.clean_otp(self.user)
        return self.cleaned_data


class TOTPDeviceForm(forms.Form):
    token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, metadata=None, **kwargs):
        super().__init__(**kwargs)
        self.fields["token"].widget.attrs.update(DEFAULT_TOKEN_WIDGET_ATTRS)
        self.user = user
        self.metadata = metadata or {}

    def clean_token(self):
        token = self.cleaned_data.get("token")

        # Find the unconfirmed device and attempt to verify the token.
        self.device = self.user.totpdevice_set.filter(confirmed=False).first()
        if not self.device.verify_token(token):
            raise forms.ValidationError(_("The entered token is not valid"))

        return token

    def save(self):
        # The device was found to be valid, delete other confirmed devices and
        # confirm the new device.
        self.user.totpdevice_set.filter(confirmed=True).delete()
        self.device.confirmed = True
        self.device.save()

        return self.device


class TOTPDeviceRemoveForm(forms.Form):

    # User must input a valid token so 2FA can be removed
    token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.fields["token"].widget.attrs.update(DEFAULT_TOKEN_WIDGET_ATTRS)

    def clean_token(self):
        # Ensure that the user has provided a valid token
        token = self.cleaned_data.get("token")

        # Verify that the user has provided a valid token
        for device in self.user.totpdevice_set.filter(confirmed=True):
            if device.verify_token(token):
                return token

        raise forms.ValidationError(_("The entered token is not valid"))

    def save(self):
        with contextlib.suppress(ObjectDoesNotExist):
            # Delete any backup tokens and their related static device.
            static_device = self.user.staticdevice_set.get(name="backup")
            static_device.token_set.all().delete()
            static_device.delete()

        # Delete TOTP device.
        device = TOTPDevice.objects.get(user=self.user)
        device.delete()
