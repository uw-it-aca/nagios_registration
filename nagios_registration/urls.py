from django.conf.urls import url
from nagios_registration.views import (
    host_group, host, service_group, service, contact_group, contact, deploy,
    ui_data, home)


urlpatterns = [
    url('^api/v1/hostgroup$', host_group),
    url('^api/v1/host/?(?P<hostname>[A-Za-z0-9\-\_\.\s]+)?$', host),
    url('^api/v1/servicegroup$', service_group),
    url('^api/v1/service$', service),
    url('^api/v1/service/(?P<hostname>[A-Za-z0-9\-\_\.\s]+)/'
        '(?P<servicename>[A-Za-z0-9\-\_\.\s]+)?$', service),
    url('^api/v1/contactgroup$', contact_group),
    url('^api/v1/contact$', contact),
    url('^api/v1/deploy$', deploy),
    url('^ui/api/v1/data', ui_data),
    url('^ui', home, name="nagios_registration_home"),
]
