def user_has_valid_totp_device(user):
    return (
        user.is_authenticated and
        user.totpdevice_set.filter(confirmed=True).exists()
    )
