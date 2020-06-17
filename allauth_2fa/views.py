from base64 import b64encode

from allauth.account import signals
from allauth.account.adapter import get_adapter
from allauth.account.utils import get_login_redirect_url

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_text
from django.views.generic import FormView, TemplateView

from django_otp.plugins.otp_static.models import StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice

from allauth_2fa import app_settings
from allauth_2fa.forms import (TOTPAuthenticateForm, TOTPDeviceForm,
                               TOTPDeviceRemoveForm)
from allauth_2fa.mixins import ValidTOTPDeviceRequiredMixin
from allauth_2fa.utils import generate_totp_config_svg_for_device, user_has_valid_totp_device


class TwoFactorAuthenticate(FormView):
    template_name = 'allauth_2fa/authenticate.' + app_settings.TEMPLATE_EXTENSION
    form_class = TOTPAuthenticateForm

    def dispatch(self, request, *args, **kwargs):
        # If the user is not about to enter their two-factor credentials,
        # redirect to the login page (they shouldn't be here!). This includes
        # anonymous users.
        if 'allauth_2fa_user_id' not in request.session:
            # Don't use the redirect_to_login here since we don't actually want
            # to include the next parameter.
            return redirect('account_login')
        return super(TwoFactorAuthenticate, self).dispatch(request, *args,
                                                           **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TwoFactorAuthenticate, self).get_form_kwargs()
        user_id = self.request.session['allauth_2fa_user_id']
        kwargs['user'] = get_user_model().objects.get(id=user_id)
        return kwargs

    def form_valid(self, form):
        """
        The allauth 2fa login flow is now done (the user logged in successfully
        with 2FA), continue the logic from allauth.account.utils.perform_login
        since it was interrupted earlier.

        """
        adapter = get_adapter(self.request)

        # Skip over the (already done) 2fa login flow and continue the original
        # allauth login flow.
        super(adapter.__class__, adapter).login(self.request, form.user)

        # Perform the rest of allauth.account.utils.perform_login, this is
        # copied from commit cedad9f156a8c78bfbe43a0b3a723c1a0b840dbd.

        # TODO Support redirect_url.
        response = HttpResponseRedirect(
            get_login_redirect_url(self.request))

        # TODO Support signal_kwargs.
        signals.user_logged_in.send(sender=form.user.__class__,
                                    request=self.request,
                                    response=response,
                                    user=form.user)

        adapter.add_message(
            self.request,
            messages.SUCCESS,
            'account/messages/logged_in.txt',
            {'user': form.user})

        return response


class TwoFactorSetup(LoginRequiredMixin, FormView):
    template_name = 'allauth_2fa/setup.' + app_settings.TEMPLATE_EXTENSION
    form_class = TOTPDeviceForm
    success_url = reverse_lazy('two-factor-backup-tokens')

    def dispatch(self, request, *args, **kwargs):
        # If the user has 2FA setup already, redirect them to the backup tokens.
        if user_has_valid_totp_device(request.user):
            return HttpResponseRedirect(reverse('two-factor-backup-tokens'))

        return super(TwoFactorSetup, self).dispatch(request, *args, **kwargs)

    def _new_device(self):
        """
        Replace any unconfirmed TOTPDevices with a new one for confirmation.

        This needs to be done whenever a GET request to the page is received OR
        if the confirmation of the device fails.
        """
        self.request.user.totpdevice_set.filter(confirmed=False).delete()
        self.device = TOTPDevice.objects.create(user=self.request.user, confirmed=False)

    def get(self, request, *args, **kwargs):
        # Whenever this page is loaded, create a new device (this ensures a
        # user's QR code isn't shown multiple times).
        self._new_device()
        return super(TwoFactorSetup, self).get(request, *args, **kwargs)

    def get_qr_code_data_uri(self):
        svg_data = generate_totp_config_svg_for_device(self.request, self.device)
        return 'data:image/svg+xml;base64,%s' % force_text(b64encode(svg_data))

    def get_context_data(self, **kwargs):
        context = super(TwoFactorSetup, self).get_context_data(**kwargs)
        context['qr_code_url'] = self.get_qr_code_data_uri()
        return context

    def get_form_kwargs(self):
        kwargs = super(TwoFactorSetup, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Confirm the device.
        form.save()
        return super(TwoFactorSetup, self).form_valid(form)

    def form_invalid(self, form):
        # If the confirmation code was wrong, generate a new device.
        self._new_device()
        return super(TwoFactorSetup, self).form_invalid(form)


class TwoFactorRemove(ValidTOTPDeviceRequiredMixin, FormView):
    template_name = 'allauth_2fa/remove.' + app_settings.TEMPLATE_EXTENSION
    form_class = TOTPDeviceRemoveForm
    success_url = reverse_lazy('two-factor-setup')

    def form_valid(self, form):
        form.save()
        return super(TwoFactorRemove, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(TwoFactorRemove, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TwoFactorBackupTokens(ValidTOTPDeviceRequiredMixin, TemplateView):
    template_name = 'allauth_2fa/backup_tokens.' + app_settings.TEMPLATE_EXTENSION
    # This can be overridden in a subclass to True,
    # to have that particular view always reveal the tokens.
    reveal_tokens = bool(app_settings.ALWAYS_REVEAL_BACKUP_TOKENS)

    def get_context_data(self, **kwargs):
        context = super(TwoFactorBackupTokens, self).get_context_data(**kwargs)
        static_device, _ = self.request.user.staticdevice_set.get_or_create(
            name='backup'
        )

        if static_device:
            context['backup_tokens'] = static_device.token_set.all()
            context['reveal_tokens'] = self.reveal_tokens

        return context

    def post(self, request, *args, **kwargs):
        static_device, _ = request.user.staticdevice_set.get_or_create(
            name='backup'
        )
        static_device.token_set.all().delete()
        for _ in range(3):
            static_device.token_set.create(token=StaticToken.random_token())
        self.reveal_tokens = True
        return self.get(request, *args, **kwargs)
