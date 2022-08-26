from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import include
from django.urls import path


def blank_view(request):
    return HttpResponse("<h1>HELLO WORLD!</h1>")


@login_required
def login_required_view(request):
    return HttpResponse(f"<h1>Hello, {request.user}</h1>")


urlpatterns = [
    # Include the allauth and 2FA urls from their respective packages.
    path("accounts/2fa/", include("allauth_2fa.urls")),
    path("accounts/", include("allauth.urls")),
    # A view without a name.
    path("unnamed-view", blank_view),
    path("login-required-view", login_required_view, name="login-required-view"),
]
