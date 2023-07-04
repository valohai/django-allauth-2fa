from allauth_2fa.forms import TOTPAuthenticateForm, TOTPDeviceForm, TOTPDeviceRemoveForm


class CustomTOTPAuthenticateForm(TOTPAuthenticateForm):
    pass


class CustomTOTPDeviceForm(TOTPDeviceForm):
    pass


class CustomTOTPDeviceRemoveForm(TOTPDeviceRemoveForm):
    pass
