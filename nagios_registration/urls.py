from django.conf.urls import patterns, url
import nagios_registration.views as views
from oauth2_provider.decorators import protected_resource
from django.contrib.auth.decorators import login_required

urlpatterns = patterns(
    'nagios_registration.views',
    url('^api/v1/host', protected_resource()(views.host)),
    url('^ui/api/v1/host', login_required(views.host), name="ui_api_host"),
    url('^ui', login_required(views.home), name="nagios_registration_home"),
    url('', 'redirect_to_home'),
)

#    url('api/v1/hostgroup', 'hostgroup'),
#    url('api/v1/service', 'service'),
#    url('api/v1/hostgroup', 'hostgroup'),
