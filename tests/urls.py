from django.http import HttpResponse
from django.urls import include
from django.urls import path


def blank_view(request):
    return HttpResponse("<h1>HELLO WORLD!</h1>")


urlpatterns = [
    # Include the allauth and 2FA urls from their respective packages.
    path("accounts/", include("allauth_2fa.urls")),
    path("accounts/", include("allauth.urls")),
    # A view without a name.
    path("unnamed-view", blank_view),
]
