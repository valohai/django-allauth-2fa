from binascii import unhexlify
from time import time

from django import forms
from django.utils.translation import ugettext_lazy as _
from django_otp.forms import OTPAuthenticationFormMixin
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice


class TOTPAuthenticateForm(OTPAuthenticationFormMixin, forms.Form):
    otp_token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, **kwargs):
        super(TOTPAuthenticateForm, self).__init__(**kwargs)
        self.fields['otp_token'].widget.attrs.update({'autofocus': 'autofocus'})
        self.user = user

    def clean(self):
        self.clean_otp(self.user)
        return self.cleaned_data


class TOTPDeviceForm(forms.Form):
    token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, key, user, metadata=None, **kwargs):
        super(TOTPDeviceForm, self).__init__(**kwargs)
        self.fields['token'].widget.attrs.update({'autofocus': 'autofocus'})
        self.key = key
        self.tolerance = 1
        self.t0 = 0
        self.step = 30
        self.drift = 0
        self.digits = 6
        self.user = user
        self.metadata = metadata or {}

    def clean_token(self):
        try:
            token = int(self.cleaned_data.get('token'))
        except ValueError:
            # valid will never equal true in this case.
            token = None
        valid = False
        t0s = [self.t0]
        key = unhexlify(self.key.encode())
        if 'valid_t0' in self.metadata:
            t0s.append(int(time()) - self.metadata['valid_t0'])
        for t0 in t0s:
            for offset in range(-self.tolerance, self.tolerance):
                expected_token = totp(
                    key,
                    self.step,
                    t0,
                    self.digits,
                    self.drift + offset
                )

                if expected_token == token:
                    self.drift = offset
                    self.metadata['valid_t0'] = int(time()) - t0
                    valid = True

        if not valid:
            raise forms.ValidationError(_('The entered token is not valid'))
        return token

    def save(self):
        return TOTPDevice.objects.create(
            user=self.user,
            key=self.key,
            tolerance=self.tolerance,
            t0=self.t0,
            step=self.step,
            drift=self.drift,
            digits=self.digits,
            name='default'
        )


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
