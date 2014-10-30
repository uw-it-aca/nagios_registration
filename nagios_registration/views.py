from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from nagios_registration.models import Host
from nagios_registration.auth import authenticate_application
import json
from oauth_provider.decorators import oauth_required


###
#
# api methods
#
###
@authenticate_application
def host(request):
    hosts = Host.objects.filter(is_active=True)

    host_list = []
    for host in hosts:
        host_list.append(host.json_data())

    return HttpResponse(json.dumps(host_list), content_type="application/json")


def redirect_to_home(request):
    return HttpResponseRedirect(reverse("nagios_registration_home"))


###
#
# Methods supporting the web ui
#
###
@login_required
def home(request):
    return render_to_response("home.html", {
        "base_url": reverse("nagios_registration_home"),
    }, RequestContext(request))


@login_required
def ui_data(request):
    hosts = Host.objects.filter(is_active=True)

    host_list = []
    for host in hosts:
        host_list.append(host.json_data())

    return HttpResponse(json.dumps(host_list), content_type="application/json")
