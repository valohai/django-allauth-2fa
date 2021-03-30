from base64 import b32encode
from io import BytesIO
from urllib.parse import quote, urlencode
from datetime import datetime, timedelta

from django.contrib.sites.shortcuts import get_current_site

import qrcode
from qrcode.image.svg import SvgPathImage
from allauth_2fa import app_settings


ATTEMPTS_CACHE = {}


def reset_device(user_id):
    """
    Returns if device has expired and updates cache
    """
    reset = False
    if user_id in ATTEMPTS_CACHE:
        if datetime.now() - timedelta(minutes=app_settings.CODE_EXPIRY_MINUTES) > ATTEMPTS_CACHE[user_id]:
            reset = True
        del ATTEMPTS_CACHE[user_id]
    ATTEMPTS_CACHE[user_id] = datetime.now()
    return reset


def minutes_to_expire(user_id):
    """
    Returns time to device resets in minutes
    """
    if user_id not in ATTEMPTS_CACHE:
        return app_settings.CODE_EXPIRY_MINUTES
    else:
        expiry_minutes_ago = datetime.now() - timedelta(minutes=app_settings.CODE_EXPIRY_MINUTES)
        last_attempt = ATTEMPTS_CACHE[user_id]
        return app_settings.CODE_EXPIRY_MINUTES if last_attempt < expiry_minutes_ago \
            else (datetime.now() - last_attempt).minute


def generate_totp_config_svg(device, issuer, label):
    params = {
        'secret': b32encode(device.bin_key).decode('utf-8'),
        'algorithm': 'SHA1',
        'digits': device.digits,
        'period': device.step,
        'issuer': issuer,
    }

    otpauth_url = 'otpauth://totp/{label}?{query}'.format(
        label=quote(label),
        query=urlencode(params),
    )

    img = qrcode.make(otpauth_url, image_factory=SvgPathImage)
    io = BytesIO()
    img.save(io)
    return io.getvalue()


def generate_totp_config_svg_for_device(request, device):
    issuer = get_current_site(request).name
    label = '{issuer}: {username}'.format(
        issuer=issuer,
        username=request.user.get_username()
    )
    return generate_totp_config_svg(device=device, issuer=issuer, label=label)


def user_has_valid_totp_device(user):
    if not user.is_authenticated:
        return False
    return user.totpdevice_set.filter(confirmed=True).exists()
