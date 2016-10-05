from django.conf.urls import include, url

urlpatterns = [
    # Include the allauth and 2FA urls from their respective packages.
    url(r'^accounts/', include('allauth_2fa.urls')),
    url(r'^accounts/', include('allauth.urls')),
]
