from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_otp.oath import TOTP


class Test2Factor(TestCase):
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

    def test_invalid_2fa_login(self):
        """Test login behavior when 2FA is configured and wrong code is given."""
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

    def test_anonymous(self):
        """
        Views should not be hittable via an AnonymousUser.
        """
        user = AnonymousUser()

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

        # Finally, the QR image view just 404s.
        resp = self.client.get(reverse('two-factor-qr-code'))
        self.assertEqual(resp.status_code, 404)
