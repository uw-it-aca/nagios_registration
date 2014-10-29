from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from nagios_registration.models import Host
import json
from oauth2_provider.decorators import protected_resource


def redirect_to_home(request):
    return HttpResponseRedirect(reverse("nagios_registration_home"))


def home(request):
    return render_to_response("home.html", {
        "base_url": reverse("nagios_registration_home"),
    }, RequestContext(request))


def host(request):
    hosts = Host.objects.filter(is_active=True)

    host_list = []
    for host in hosts:
        host_list.append(host.json_data())

    return HttpResponse(json.dumps(host_list), content_type="application/json")


def _get_user_for_oauth_request(request):
    from oauth2_provider.oauth2_backends import get_oauthlib_core
    oauthlib_core = get_oauthlib_core()
    valid, r = oauthlib_core.verify_request(request, scopes=[])
    return r.user
