from django.conf.urls import include, url
from django.http import HttpResponse


def blank_view(request):
    return HttpResponse("<h1>HELLO WORLD!</h1>")


urlpatterns = [
    # Include the allauth and 2FA urls from their respective packages.
    url(r'^accounts/', include('allauth_2fa.urls')),
    url(r'^accounts/', include('allauth.urls')),

    # A view without a name.
    url(r"^unnamed-view$", blank_view),
]
