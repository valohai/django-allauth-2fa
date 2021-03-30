from base64 import b32encode
from io import BytesIO
from urllib.parse import quote
from urllib.parse import urlencode

import qrcode
from django.contrib.sites.shortcuts import get_current_site
from qrcode.image.svg import SvgPathImage


def get_device_base32_secret(device):
    return b32encode(device.bin_key).decode("utf-8")


def generate_totp_config_svg(device, issuer, label):
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


def generate_totp_config_svg_for_device(request, device):
    issuer = get_current_site(request).name
    label = f"{issuer}: {request.user.get_username()}"
    return generate_totp_config_svg(device=device, issuer=issuer, label=label)


def user_has_valid_totp_device(user):
    if not user.is_authenticated:
        return False
    return user.totpdevice_set.filter(confirmed=True).exists()
