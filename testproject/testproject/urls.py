from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(
        r'^accounts/profile',
        TemplateView.as_view(template_name='profile.html'),
        name='profile',
    ),
    url(r'^accounts/', include('allauth_2fa.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
