from __future__ import annotations

from base64 import b32encode
from io import BytesIO
from urllib.parse import quote
from urllib.parse import urlencode

import qrcode
from django_otp.models import Device
from qrcode.image.svg import SvgPathImage


def get_device_base32_secret(device: Device) -> str:
    return b32encode(device.bin_key).decode("utf-8")


def generate_totp_config_svg(device: Device, issuer: str, label: str) -> bytes:
    params = {
        "secret": get_device_base32_secret(device),
        "algorithm": "SHA1",
        "digits": device.digits,
        "period": device.step,
        "issuer": issuer,
    }

    otpauth_url = f"otpauth://totp/{quote(label)}?{urlencode(params)}"

    img = qrcode.make(otpauth_url, image_factory=SvgPathImage)
    io = BytesIO()
    img.save(io)
    return io.getvalue()


def user_has_valid_totp_device(user) -> bool:
    if not user.is_authenticated:
        return False
    return user.totpdevice_set.filter(confirmed=True).exists()
