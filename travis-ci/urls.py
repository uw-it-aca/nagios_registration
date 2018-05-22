from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^oauth/', include('oauth_provider.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('nagios_registration.urls')),
]
