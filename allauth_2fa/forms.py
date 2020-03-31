from django import forms
from django.utils.translation import gettext_lazy as _

from django_otp.forms import OTPAuthenticationFormMixin
from django_otp.plugins.otp_totp.models import TOTPDevice


class TOTPAuthenticateForm(OTPAuthenticationFormMixin, forms.Form):
    otp_token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, **kwargs):
        super(TOTPAuthenticateForm, self).__init__(**kwargs)
        self.fields['otp_token'].widget.attrs.update({
            'autofocus': 'autofocus',
            'autocomplete': 'off',
            'inputmode': 'numeric',
        })
        self.user = user

    def clean(self):
        self.clean_otp(self.user)
        return self.cleaned_data


class TOTPDeviceForm(forms.Form):
    token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, metadata=None, **kwargs):
        super(TOTPDeviceForm, self).__init__(**kwargs)
        self.fields['token'].widget.attrs.update({
            'autofocus': 'autofocus',
            'autocomplete': 'off',
        })
        self.user = user
        self.metadata = metadata or {}

    def clean_token(self):
        token = self.cleaned_data.get('token')

        # Find the unconfirmed device and attempt to verify the token.
        self.device = self.user.totpdevice_set.filter(confirmed=False).first()
        if not self.device.verify_token(token):
            raise forms.ValidationError(_('The entered token is not valid'))

        return token

    def save(self):
        # The device was found to be valid, delete other confirmed devices and
        # confirm the new device.
        self.user.totpdevice_set.filter(confirmed=True).delete()
        self.device.confirmed = True
        self.device.save()

        return self.device


class TOTPDeviceRemoveForm(forms.Form):

    def __init__(self, user, **kwargs):
        super(TOTPDeviceRemoveForm, self).__init__(**kwargs)
        self.user = user

    def save(self):
        # Delete any backup tokens.
        static_device = self.user.staticdevice_set.get(name='backup')
        static_device.token_set.all().delete()
        static_device.delete()

        # Delete TOTP device.
        device = TOTPDevice.objects.get(user=self.user)
        device.delete()
