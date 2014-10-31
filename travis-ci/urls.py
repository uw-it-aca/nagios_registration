from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^oauth/', include('oauth_provider.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('nagios_registration.urls')),
)
