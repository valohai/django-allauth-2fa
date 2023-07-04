from __future__ import annotations

from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from allauth_2fa.utils import user_has_valid_totp_device


class ValidTOTPDeviceRequiredMixin(AccessMixin):
    no_valid_totp_device_url = reverse_lazy("two-factor-setup")

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not user_has_valid_totp_device(request.user):
            return self.handle_missing_totp_device()
        return super().dispatch(request, *args, **kwargs)

    def handle_missing_totp_device(self) -> HttpResponse:
        return HttpResponseRedirect(self.no_valid_totp_device_url)
