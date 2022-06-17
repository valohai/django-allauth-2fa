from typing import Callable
from typing import Optional
from typing import Tuple
from unittest.mock import Mock

import pytest
from allauth.account.signals import user_logged_in
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import override_settings
from django.urls import reverse
from django.urls import reverse_lazy
from django_otp.oath import TOTP
from django_otp.plugins.otp_totp.models import TOTPDevice
from pytest_django.asserts import assertRedirects

from allauth_2fa.middleware import BaseRequire2FAMiddleware

ADAPTER_CLASSES = [
    "allauth_2fa.adapter.OTPAdapter",
    "tests.adapter.CustomAdapter",
]

TWO_FACTOR_AUTH_URL = reverse_lazy("two-factor-authenticate")
TWO_FACTOR_SETUP_URL = reverse_lazy("two-factor-setup")
LOGIN_URL = reverse_lazy("account_login")
JOHN_CREDENTIALS = {"login": "john", "password": "doe"}


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def pytest_generate_tests(metafunc):
    if "adapter" in metafunc.fixturenames:
        metafunc.parametrize("adapter", ADAPTER_CLASSES, indirect=True)


@pytest.fixture(autouse=True)
def adapter(request, settings):
    settings.ACCOUNT_ADAPTER = request.param
    # Can be used to verify the class is correct:
    # assert get_adapter().__class__.__name__ == request.param.rpartition(".")[-1]


@pytest.fixture()
def john() -> "AbstractUser":
    user = get_user_model().objects.create(username="john")
    user.set_password("doe")
    user.save()
    return user


@pytest.fixture()
def john_with_totp(john: AbstractUser) -> Tuple[AbstractUser, TOTPDevice]:
    totp_model = john.totpdevice_set.create()
    return (john, totp_model)


@pytest.fixture()
def user_logged_in_count(request) -> Callable[[], int]:
    login_callback = Mock()
    user_logged_in.connect(login_callback)
    request.addfinalizer(lambda: user_logged_in.disconnect(login_callback))

    def get_login_count() -> int:
        return login_callback.call_count

    return get_login_count


def login(client, *, expected_redirect_url: Optional[str], credentials=None):
    if credentials is None:
        credentials = JOHN_CREDENTIALS
    resp = client.post(LOGIN_URL, credentials)
    if expected_redirect_url:
        assertRedirects(resp, expected_redirect_url, fetch_redirect_response=False)


def get_token_from_totp_device(totp_model) -> str:
    return TOTP(
        key=totp_model.bin_key,
        step=totp_model.step,
        t0=totp_model.t0,
        digits=totp_model.digits,
    ).token()


def do_totp_authentication(
    client,
    totp_device: TOTPDevice,
    *,
    expected_redirect_url: Optional[str],
    auth_url: str = TWO_FACTOR_AUTH_URL,
):
    token = get_token_from_totp_device(totp_device)
    resp = client.post(auth_url, {"otp_token": token})
    if expected_redirect_url:
        assertRedirects(resp, expected_redirect_url, fetch_redirect_response=False)


def test_standard_login(client, john, user_logged_in_count):
    """Test login behavior when 2FA is not configured."""
    login(client, expected_redirect_url=settings.LOGIN_REDIRECT_URL)

    # Ensure the signal is received as expected.
    assert user_logged_in_count() == 1


def test_2fa_login(client, john_with_totp, user_logged_in_count):
    """Test login behavior when 2FA is configured."""
    user, totp_device = john_with_totp
    login(client, expected_redirect_url=TWO_FACTOR_AUTH_URL)

    # Ensure no signal is received yet.
    assert user_logged_in_count() == 0

    # Now ensure that logging in actually works.
    do_totp_authentication(
        client,
        totp_device=totp_device,
        expected_redirect_url=settings.LOGIN_REDIRECT_URL,
    )

    # Ensure the signal is received as expected.
    assert user_logged_in_count() == 1


def test_invalid_2fa_login(client, john_with_totp):
    """Test login behavior when 2FA is configured and wrong code is given."""
    login(client, expected_redirect_url=TWO_FACTOR_AUTH_URL)

    # Ensure that logging in does not work with invalid token
    resp = client.post(TWO_FACTOR_AUTH_URL, {"otp_token": "invalid"})
    assert resp.status_code == 200

    # Check the user did not get logged in
    url = reverse("login-required-view")
    resp = client.get(url)
    assertRedirects(resp, f"{LOGIN_URL}?next={url}")


def test_2fa_redirect(client, john):
    """
    Going to the 2FA login page when not logged in (or when fully logged in)
    should redirect.
    """

    # Not logged in.
    resp = client.get(TWO_FACTOR_AUTH_URL)
    assertRedirects(resp, LOGIN_URL, fetch_redirect_response=False)

    login(client, expected_redirect_url=settings.LOGIN_REDIRECT_URL)

    resp = client.get(TWO_FACTOR_AUTH_URL)
    assertRedirects(resp, LOGIN_URL, fetch_redirect_response=False)


@pytest.mark.parametrize("target_url", [LOGIN_URL, "/unnamed-view"])
def test_2fa_reset_flow(client, john_with_totp, target_url):
    """
    Ensure the login flow is reset when navigating away before entering
    two-factor credentials.
    """
    login(client, expected_redirect_url=TWO_FACTOR_AUTH_URL)

    # The user ID should be in the session.
    assert client.session.get("allauth_2fa_user_id")

    # Navigate to a different page.
    client.get(target_url)

    # The middleware should reset the login flow.
    assert not client.session.get("allauth_2fa_user_id")

    # Trying to continue with two-factor without logging in again will
    # redirect to login.
    resp = client.get(TWO_FACTOR_AUTH_URL)

    assertRedirects(resp, LOGIN_URL, fetch_redirect_response=False)


def test_2fa_removal(client, john_with_totp):
    """Removing 2FA should be possible."""
    user, totp_device = john_with_totp
    login(client, expected_redirect_url=TWO_FACTOR_AUTH_URL)
    do_totp_authentication(
        client,
        totp_device=totp_device,
        expected_redirect_url=settings.LOGIN_REDIRECT_URL,
    )
    assert user.totpdevice_set.exists()

    # Navigate to 2FA removal view
    client.get(reverse("two-factor-remove"))

    # reset throttling and get another token
    totp_device.throttle_reset()
    token = get_token_from_totp_device(totp_device)

    # ... and POST to confirm
    client.post(reverse("two-factor-remove"), {"token": token})

    assert not user.totpdevice_set.exists()


@pytest.mark.parametrize("next_via", ["get", "post"])
def test_2fa_login_forwarding_get_parameters(client, john_with_totp, next_via: str):
    """
    Test that the 2FA workflow passes forward the GET parameters sent to the
    TwoFactorAuthenticate view.
    """

    # Add a next to unnamed-view.
    if next_via == "post":
        resp = client.post(
            LOGIN_URL + "?existing=param",
            {**JOHN_CREDENTIALS, "next": "unnamed-view"},
            follow=True,
        )
    else:
        resp = client.post(
            LOGIN_URL + "?existing=param&next=unnamed-view",
            JOHN_CREDENTIALS,
            follow=True,
        )

    # Ensure that the unnamed-view is still being forwarded to.
    assertRedirects(
        resp,
        TWO_FACTOR_AUTH_URL + "?existing=param&next=unnamed-view",
        fetch_redirect_response=False,
    )


def test_anonymous(client):
    """
    Views should not be hittable via an AnonymousUser.
    """
    # The authentication page redirects to the login page.
    resp = client.get(TWO_FACTOR_AUTH_URL)
    assertRedirects(resp, LOGIN_URL, fetch_redirect_response=False)

    # Some pages redirect to the login page and then will redirect back.
    for url in [
        "two-factor-setup",
        "two-factor-backup-tokens",
        "two-factor-remove",
    ]:
        url = reverse(url)
        resp = client.get(url)
        assertRedirects(
            resp,
            LOGIN_URL + "?next=" + url,
            fetch_redirect_response=False,
        )


def test_backwards_compatible_url(client, john_with_totp, user_logged_in_count):
    """Ensure that the old 2FA URLs still work."""
    # TODO(1.0): remove this test
    user, totp_device = john_with_totp
    login(client, expected_redirect_url=TWO_FACTOR_AUTH_URL)
    # The old URL doesn't have a trailing slash.
    do_totp_authentication(
        client,
        totp_device=totp_device,
        auth_url=str(TWO_FACTOR_AUTH_URL).rstrip("/"),
        expected_redirect_url=settings.LOGIN_REDIRECT_URL,
    )

    # Ensure the signal is received as expected.
    assert user_logged_in_count() == 1


def test_not_configured_redirect(client, john):
    """Viewing backup codes or disabling 2FA should redirect if 2FA is not
    configured."""
    login(client, expected_redirect_url=settings.LOGIN_REDIRECT_URL)

    # The 2FA pages should redirect.
    for url_name in ["two-factor-backup-tokens", "two-factor-remove"]:
        resp = client.get(reverse(url_name))
        assertRedirects(resp, TWO_FACTOR_SETUP_URL, fetch_redirect_response=False)


class Require2FA(BaseRequire2FAMiddleware):
    def require_2fa(self, request):
        return True


@pytest.mark.parametrize("with_messages", (False, True))
def test_require_2fa_middleware(client, john, settings, with_messages):
    new_middleware = [
        # Add the middleware that requires 2FA.
        "tests.test_allauth_2fa.Require2FA",
    ]
    new_installed_apps = []

    if with_messages:
        new_middleware.append("django.contrib.messages.middleware.MessageMiddleware")
        new_installed_apps.append("django.contrib.messages")

    with override_settings(
        # Don't redirect to an "allowed" URL.
        LOGIN_REDIRECT_URL="/unnamed-view",
        MIDDLEWARE=settings.MIDDLEWARE + tuple(new_middleware),
        INSTALLED_APPS=settings.INSTALLED_APPS + tuple(new_installed_apps),
    ):
        resp = client.post(LOGIN_URL, JOHN_CREDENTIALS, follow=True)
        # The user is redirected to the 2FA setup page.
        # (In particular, see that the last redirect brought us to the 2FA setup page.)
        assert resp.redirect_chain[-1][0] == TWO_FACTOR_SETUP_URL
        # TODO: check messages?
