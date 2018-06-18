from django.conf.urls import url
from nagios_registration.views import (
    host_group, host, service_group, service, contact_group, contact, deploy,
    home)


urlpatterns = [
    url(r'^api/v1/hostgroup$', host_group),
    url(r'^api/v1/host/?(?P<hostname>[A-Za-z0-9\-\_\.\s]+)?$', host),
    url(r'^api/v1/servicegroup$', service_group),
    url(r'^api/v1/service$', service),
    url(r'^api/v1/service/(?P<hostname>[A-Za-z0-9\-\_\.\s]+)/'
        r'(?P<servicename>[A-Za-z0-9%~\/\-\_\.\s]+)?$', service),
    url(r'^api/v1/contactgroup$', contact_group),
    url(r'^api/v1/contact$', contact),
    url(r'^api/v1/deploy$', deploy),
    url(r'^ui', home, name="nagios_registration_home"),
]
