from allauth_2fa.forms import TOTPAuthenticateForm
from allauth_2fa.forms import TOTPDeviceForm
from allauth_2fa.forms import TOTPDeviceRemoveForm


class CustomTOTPAuthenticateForm(TOTPAuthenticateForm):
    pass


class CustomTOTPDeviceForm(TOTPDeviceForm):
    pass


class CustomTOTPDeviceRemoveForm(TOTPDeviceRemoveForm):
    pass
