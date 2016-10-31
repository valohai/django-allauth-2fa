from django.conf.urls import include, url

from allauth_2fa import views

urlpatterns = [
    # Include the allauth and 2FA urls from their respective packages.
    url(r'^accounts/', include('allauth_2fa.urls')),
    url(r'^accounts/', include('allauth.urls')),

    # A view without a name.
    url(r"^unnamed-view$", views.TwoFactorAuthenticate.as_view()),
]
