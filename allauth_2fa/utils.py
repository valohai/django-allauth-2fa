from base64 import b32encode
from io import BytesIO
from urllib.parse import quote, urlencode
from datetime import datetime, timedelta

from django.contrib.sites.shortcuts import get_current_site

import qrcode
from django.contrib.sites.shortcuts import get_current_site
from qrcode.image.svg import SvgPathImage
from allauth_2fa import app_settings


ATTEMPTS_CACHE = {}


def reset_device(user_id):
    """
    Returns if device has expired and updates cache
    """
    reset = False
    if user_id in ATTEMPTS_CACHE:
        if code_has_expired(user_id):
            reset = True
        del ATTEMPTS_CACHE[user_id]
    ATTEMPTS_CACHE[user_id] = datetime.now()
    return reset


def code_has_expired(user_id):
    return datetime.now() - timedelta(minutes=app_settings.CODE_EXPIRY_MINUTES) > ATTEMPTS_CACHE[user_id]


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
