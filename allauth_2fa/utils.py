from base64 import b32encode
from io import BytesIO
from urllib.parse import quote, urlencode
from datetime import datetime, timedelta

from django.contrib.sites.shortcuts import get_current_site

import qrcode
from qrcode.image.svg import SvgPathImage
from app_settings import CODE_EXPIRY_MINUTES


QRCODE_CACHE = {}


def qr_code_expired():
    last_access = QRCODE_CACHE.get('time')
    if last_access and datetime.now() - timedelta(minutes=CODE_EXPIRY_MINUTES) > last_access:
        return True
    else:
        return False


def cache_qr_code(code):
    QRCODE_CACHE['code'] = code
    QRCODE_CACHE['time'] = datetime.now()


def get_cached_qr_code():
    return QRCODE_CACHE.get('code')


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
