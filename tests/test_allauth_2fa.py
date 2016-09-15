from django.conf import settings
from django.contrib.auth import get_user_model
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

        # Now ensure that logging in actually works.
        resp = self.client.post(reverse('two-factor-authenticate'),
                                {'otp_token': 'invalid'})
        self.assertEqual(resp.status_code, 200)

    def test_2fa_reset_flow(self):
        """Test login flow reset when navigating away."""
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

        self.assertIn('allauth_2fa_user_id', self.client.session)
        # Navigate back to login
        self.client.get(reverse('account_login'))
        self.assertNotIn('allauth_2fa_user_id', self.client.session)

        # And try to continue with two-factor without logging in again
        resp = self.client.get(reverse('two-factor-authenticate'))

        self.assertRedirects(resp,
                             reverse('account_login'),
                             fetch_redirect_response=False)
