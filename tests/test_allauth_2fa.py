from urllib.parse import (
    parse_qsl, urlencode, urlparse, urlunparse
)

from allauth.account.signals import user_logged_in

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings, TestCase
from django.urls import reverse

from django_otp.oath import TOTP

from allauth_2fa.middleware import BaseRequire2FAMiddleware


def normalize_url(url):
    """Sort the URL's query string parameters."""
    url = str(url)  # Coerce reverse_lazy() URLs.
    scheme, netloc, path, params, query, fragment = urlparse(url)
    query_parts = sorted(parse_qsl(query))
    return urlunparse((scheme, netloc, path, params, urlencode(query_parts), fragment))


class Test2Factor(TestCase):
    def setUp(self):
        # Track the signals sent via allauth.
        self.user_logged_in_count = 0
        user_logged_in.connect(self._login_callback)

    def _login_callback(self, sender, **kwargs):
        self.user_logged_in_count += 1

    def test_standard_login(self):
        """Test login behavior when 2FA is not configured."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp,
                             settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)

        # Ensure the signal is received as expected.
        self.assertEqual(self.user_logged_in_count, 1)

    def test_2fa_login(self):
        """Test login behavior when 2FA is configured."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        totp_model = user.totpdevice_set.create()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp,
                             reverse('two-factor-authenticate'),
                             fetch_redirect_response=False)

        # Now ensure that logging in actually works.
        totp = TOTP(totp_model.bin_key, totp_model.step, totp_model.t0, totp_model.digits)
        resp = self.client.post(reverse('two-factor-authenticate'),
                                {'otp_token': totp.token()})
        self.assertRedirects(resp,
                             settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)

        # Ensure the signal is received as expected.
        self.assertEqual(self.user_logged_in_count, 1)

    def test_invalid_2fa_login(self):
        """Test login behavior when 2FA is configured and wrong code is given."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        user.totpdevice_set.create()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp,
                             reverse('two-factor-authenticate'),
                             fetch_redirect_response=False)

        # Ensure that logging in does not work with invalid token
        resp = self.client.post(reverse('two-factor-authenticate'),
                                {'otp_token': 'invalid'})
        self.assertEqual(resp.status_code, 200)

    def test_2fa_redirect(self):
        """
        Going to the 2FA login page when not logged in (or when fully logged in)
        should redirect.
        """
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()

        # Not logged in.
        resp = self.client.get(reverse('two-factor-authenticate'))
        self.assertRedirects(resp,
                             reverse('account_login'),
                             fetch_redirect_response=False)

        # Logged in.
        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})

        resp = self.client.get(reverse('two-factor-authenticate'))
        self.assertRedirects(resp,
                             reverse('account_login'),
                             fetch_redirect_response=False)

    def test_2fa_reset_flow(self):
        """
        Ensure the login flow is reset when navigating away before entering
        two-factor credentials.
        """
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        user.totpdevice_set.create()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp,
                             reverse('two-factor-authenticate'),
                             fetch_redirect_response=False)

        # The user ID should be in the session.
        self.assertIn('allauth_2fa_user_id', self.client.session)

        # Navigate to a different page.
        self.client.get(reverse('account_login'))

        # The middleware should reset the login flow.
        self.assertNotIn('allauth_2fa_user_id', self.client.session)

        # Trying to continue with two-factor without logging in again will
        # redirect to login.
        resp = self.client.get(reverse('two-factor-authenticate'))

        self.assertRedirects(resp,
                             reverse('account_login'),
                             fetch_redirect_response=False)

    def test_2fa_login_forwarding_get_parameters(self):
        """
        Test that the 2FA workflow passes forward the GET parameters sent to the
        TwoFactorAuthenticate view.
        """
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        user.totpdevice_set.create()

        # Add a next to unnamed-view.
        resp = self.client.post(reverse('account_login') + '?existing=param&next=unnamed-view',
                                {'login': 'john',
                                 'password': 'doe'}, follow=True)

        # Ensure that the unnamed-view is still being forwarded to.
        resp.redirect_chain[-1] = (normalize_url(resp.redirect_chain[-1][0]), resp.redirect_chain[-1][1])
        self.assertRedirects(
            resp,
            normalize_url(reverse('two-factor-authenticate') + '?existing=param&next=unnamed-view'),
            fetch_redirect_response=False)

    def test_2fa_login_forwarding_next_via_post(self):
        """
        Test that the 2FA workflow passes forward to next via POST parameters sent to the
        TwoFactorAuthenticate view.
        """
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        user.totpdevice_set.create()

        # Add a next to unnamed-view.
        resp = self.client.post(reverse('account_login') + '?existing=param',
                                {'login': 'john',
                                 'password': 'doe',
                                 'next': 'unnamed-view'}, follow=True)

        # Ensure that the unnamed-view is still being forwarded to, preserving existing query params.
        resp.redirect_chain[-1] = (normalize_url(resp.redirect_chain[-1][0]), resp.redirect_chain[-1][1])
        self.assertRedirects(
            resp,
            normalize_url(reverse('two-factor-authenticate') + '?existing=param&next=unnamed-view'),
            fetch_redirect_response=False)

    def test_anonymous(self):
        """
        Views should not be hittable via an AnonymousUser.
        """
        # The authentication page redirects to the login page.
        url = reverse('two-factor-authenticate')
        resp = self.client.get(url)
        self.assertRedirects(resp,
                             reverse('account_login'),
                             fetch_redirect_response=False)

        # Some pages redirect to the login page and then will redirect back.
        for url in ['two-factor-setup', 'two-factor-backup-tokens', 'two-factor-remove']:
            url = reverse(url)
            resp = self.client.get(url)
            self.assertRedirects(resp,
                                 reverse('account_login') + '?next=' + url,
                                 fetch_redirect_response=False)

    def test_unnamed_view(self):
        """Views without names should not throw an exception."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        user.totpdevice_set.create()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp,
                             reverse('two-factor-authenticate'),
                             fetch_redirect_response=False)

        # The user ID should be in the session.
        self.assertIn('allauth_2fa_user_id', self.client.session)

        # Navigate to a different (unnamed) page.
        resp = self.client.get('/unnamed-view')

        # The middleware should reset the login flow.
        self.assertNotIn('allauth_2fa_user_id', self.client.session)

        # Trying to continue with two-factor without logging in again will
        # redirect to login.
        resp = self.client.get(reverse('two-factor-authenticate'))

        self.assertRedirects(resp,
                             reverse('account_login'),
                             fetch_redirect_response=False)

    def test_backwards_compatible_url(self):
        """Ensure that the old 2FA URLs still work."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        totp_model = user.totpdevice_set.create()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp,
                             reverse('two-factor-authenticate'),
                             fetch_redirect_response=False)

        # Now ensure that logging in actually works.
        totp = TOTP(totp_model.bin_key, totp_model.step, totp_model.t0, totp_model.digits)

        # The old URL doesn't have a trailing slash.
        url = reverse('two-factor-authenticate').rstrip('/')

        resp = self.client.post(url, {'otp_token': totp.token()})
        self.assertRedirects(resp,
                             settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)

        # Ensure the signal is received as expected.
        self.assertEqual(self.user_logged_in_count, 1)

    def test_not_configured_redirect(self):
        """Viewing backup codes or disabling 2FA should redirect if 2FA is not configured."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()

        # Login
        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})

        # The 2FA pages should redirect.
        for url_name in ['two-factor-backup-tokens', 'two-factor-remove']:
            resp = self.client.get(reverse(url_name))
            self.assertRedirects(resp,
                                 reverse('two-factor-setup'),
                                 fetch_redirect_response=False)


class Require2FA(BaseRequire2FAMiddleware):
    def require_2fa(self, request):
        return True


@override_settings(
    # Don't redirect to an "allowed" URL.
    LOGIN_REDIRECT_URL='/unnamed-view',
    # Add the middleware that requires 2FA.
    MIDDLEWARE=settings.MIDDLEWARE + ('tests.test_allauth_2fa.Require2FA',)
)
class TestRequire2FAMiddleware(TestCase):
    def test_no_2fa(self):
        """Test login behavior when 2FA is not configured."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'},
                                follow=True)
        # The user is redirected to the 2FA setup page.
        self.assertRedirects(resp,
                             reverse('two-factor-setup'),
                             fetch_redirect_response=False)

    def test_2fa(self):
        """Test login behavior when 2FA is configured."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        totp_model = user.totpdevice_set.create()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp,
                             reverse('two-factor-authenticate'),
                             fetch_redirect_response=False)

        # Now ensure that logging in actually works.
        totp = TOTP(totp_model.bin_key, totp_model.step, totp_model.t0, totp_model.digits)
        resp = self.client.post(reverse('two-factor-authenticate'),
                                {'otp_token': totp.token()})
        # The user ends up on the normal redirect login page.
        self.assertRedirects(resp,
                             settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)

    @override_settings(
        INSTALLED_APPS=settings.INSTALLED_APPS + ('django.contrib.messages', ),
        # This doesn't seem to stack nicely with the class-based one, so add the
        # middleware here.
        MIDDLEWARE=settings.MIDDLEWARE + (
            'tests.test_allauth_2fa.Require2FA',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
    )
    def test_no_2fa_messages(self):
        """Test login behavior when 2FA is not configured and the messages framework is in use."""
        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()

        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'},
                                follow=True)

        # The user is redirected to the 2FA setup page.
        self.assertRedirects(resp,
                             reverse('two-factor-setup'),
                             fetch_redirect_response=False)
