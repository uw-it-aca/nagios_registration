from django.conf.urls import patterns, url
import nagios_registration.views as views

urlpatterns = patterns(
    'nagios_registration.views',
    url('^api/v1/hostgroup$', views.host_group),
    url('^api/v1/host/?(?P<hostname>[A-Za-z0-9\-\_\.\s]+)?$', views.host),
    url('^api/v1/servicegroup$', views.service_group),
    url('^api/v1/service$', views.service),
    url('^api/v1/contactgroup$', views.contact_group),
    url('^api/v1/contact$', views.contact),
    url('^api/v1/deploy$', views.deploy),
    url('^ui/api/v1/data', views.ui_data),
    url('^ui/api/v1/host/?(?P<hostname>[A-Za-z0-9\-\_\.\s]+)?$',
        views.ui_host),
    url('^ui', views.home, name="nagios_registration_home"),
    url('', 'redirect_to_home'),
)

#    url('api/v1/hostgroup', 'hostgroup'),
#    url('api/v1/service', 'service'),
#    url('api/v1/hostgroup', 'hostgroup'),
