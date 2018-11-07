from base64 import b32encode

from django.utils.six import BytesIO
import qrcode
from qrcode.image.svg import SvgPathImage

try:
    from urllib.parse import quote, urlencode
except ImportError:
    from urllib import quote, urlencode



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


def user_has_valid_totp_device(user):
    return (
        user.is_authenticated and
        user.totpdevice_set.filter(confirmed=True).exists()
    )
