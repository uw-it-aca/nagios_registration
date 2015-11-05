from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from nagios_registration.models import Host, HostGroup, Service, ServiceGroup
from nagios_registration.models import Contact, ContactGroup
from nagios_registration.auth import authenticate_application
from nagios_registration.util import generate_configuration
import json
from oauth_provider.decorators import oauth_required
import os


###
#
# api methods
#
###
@csrf_exempt
@authenticate_application
def deploy(request):
    if request.method == "POST":
        if not hasattr(settings, "NAGIOS_CONFIGURATION_FILE"):
            msg = "Missing setting: NAGIOS_CONFIGURATION_FILE"
            response = HttpResponse(msg)
            response.status_code = 500
            return response

        if not hasattr(settings, "NAGIOS_RESTART_COMMAND"):
            response = HttpResponse("Missing setting: NAGIOS_RESTART_COMMAND")
            response.status_code = 500
            return response

        configuration = generate_configuration()
        f = open(settings.NAGIOS_CONFIGURATION_FILE, "w")
        f.write(configuration)
        f.close()

        os.system(settings.NAGIOS_RESTART_COMMAND)

        return HttpResponse("OK")


@csrf_exempt
@authenticate_application
def host(request, hostname=None):
    def _get(request):
        hosts = Host.objects.filter(is_active=True)
        host_list = []
        for host in hosts:
            host_list.append(host.json_data())

        return HttpResponse(json.dumps(host_list),
                            content_type="application/json")

    def _post(request):
        try:
            json_data = json.loads(request.body)
            name = json_data["name"]
            address = json_data["address"]
            contact_groups = json_data["contact_groups"]

            try:
                host = Host.objects.get(name=name)
                host.address = address
                host.contact_groups = contact_groups
                host.save()
            except Host.DoesNotExist:
                host = Host.objects.create(name=name,
                                           address=address,
                                           contact_groups=contact_groups,
                                           )

            response = HttpResponse(json.dumps(host.json_data()))
            response.status_code = 201
            return response

        except Exception as ex:
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    def _delete(request, hostname):
        try:
            host = Host.objects.get(address=hostname)
            host.delete()

            response = HttpResponse(json.dumps(host.json_data()),
                                    content_type="application/json")

        except Host.DoesNotExist:
            response = HttpResponse("Not Found", status=404)

        except Exception as ex:
            response = HttpResponse(ex, status=500)

        return response

    if request.method == "GET":
        return _get(request)

    elif request.method == "POST":
        return _post(request)

    elif request.method == "DELETE":
        return _delete(request, hostname)


@csrf_exempt
@authenticate_application
def host_group(request):
    def _get(request):
        hostgroups = HostGroup.objects.all()
        hostgroup_list = []
        for group in hostgroups:
            hostgroup_list.append(group.json_data())

        return HttpResponse(json.dumps(hostgroup_list),
                            content_type="application/json")

    def _post(request):
        try:
            json_data = json.loads(request.body)
            name = json_data["name"]
            alias = json_data["alias"]

            new_group, created = HostGroup.objects.get_or_create(name=name,
                                                                 alias=alias,
                                                                 )

            response = HttpResponse(json.dumps(new_group.json_data()))
            response.status_code = 201
            return response

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    def _patch(request):
        try:
            json_data = json.loads(request.body)
            hostname = json_data["host"]
            groupname = json_data["group"]

            group = HostGroup.objects.get(name=groupname)
            host = Host.objects.get(name=hostname)

            group.hosts.add(host)

            return HttpResponse("")

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    if request.method == "GET":
        return _get(request)

    if request.method == "POST":
        return _post(request)

    if request.method == "PATCH":
        return _patch(request)


@csrf_exempt
@authenticate_application
def service(request):
    def _get(request):
        services = Service.objects.all()
        services_list = []
        for service in services:
            services_list.append(service.json_data())

        return HttpResponse(json.dumps(services_list),
                            content_type="application/json")

    def _post(request):
        try:
            json_data = json.loads(request.body)

            bs = json_data["base_service"]
            desc = json_data["description"]
            cc = json_data["check_command"]

            cg = None
            if "contact_groups" in json_data:
                cg = json_data["contact_groups"]

            try:
                service = Service.objects.get(description=desc)
                service.base_service = bs
                service.contact_groups = cg
                service.check_command = cc
                service.save()
            except Service.DoesNotExist:
                service = Service.objects.create(base_service=bs,
                                                 description=desc,
                                                 contact_groups=cg,
                                                 check_command=cc,
                                                 )

            response = HttpResponse(json.dumps(service.json_data()))
            response.status_code = 201
            return response

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    def _patch(request):
        try:
            json_data = json.loads(request.body)
            hostname = json_data["host"]
            servicename = json_data["service"]

            service = Service.objects.get(description=servicename)
            host = Host.objects.get(name=hostname)

            service.hosts.add(host)

            return HttpResponse("")

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    if request.method == "GET":
        return _get(request)

    if request.method == "POST":
        return _post(request)

    if request.method == "PATCH":
        return _patch(request)


@csrf_exempt
@authenticate_application
def service_group(request):
    def _get(request):
        servicegroups = ServiceGroup.objects.all()
        servicegroup_list = []
        for group in servicegroups:
            servicegroup_list.append(group.json_data())

        return HttpResponse(json.dumps(servicegroup_list),
                            content_type="application/json")

    def _post(request):
        try:
            json_data = json.loads(request.body)
            name = json_data["name"]
            alias = json_data["alias"]

            new_group, is_new = ServiceGroup.objects.get_or_create(name=name,
                                                                   alias=alias,
                                                                   )

            response = HttpResponse(json.dumps(new_group.json_data()))
            response.status_code = 201
            return response

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    def _patch(request):
        try:
            json_data = json.loads(request.body)
            servicename = json_data["service"]
            groupname = json_data["group"]

            group = ServiceGroup.objects.get(name=groupname)
            service = Service.objects.get(description=servicename)

            group.services.add(service)

            return HttpResponse("")

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    if request.method == "GET":
        return _get(request)

    if request.method == "POST":
        return _post(request)

    if request.method == "PATCH":
        return _patch(request)


@csrf_exempt
@authenticate_application
def contact(request):
    def _get(request):
        contacts = Contact.objects.all()
        contacts_list = []
        for contact in contacts:
            contacts_list.append(contact.json_data())

        return HttpResponse(json.dumps(contacts_list),
                            content_type="application/json")

    def _post(request):
        try:
            json_data = json.loads(request.body)

            name = json_data["name"]
            email = json_data["email"]

            new_contact, new = Contact.objects.get_or_create(name=name,
                                                             email=email,
                                                             )

            response = HttpResponse(json.dumps(new_contact.json_data()))
            response.status_code = 201
            return response

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    if request.method == "GET":
        return _get(request)

    if request.method == "POST":
        return _post(request)


@csrf_exempt
@authenticate_application
def contact_group(request):
    def _get(request):
        contactgroups = ContactGroup.objects.all()
        contactgroup_list = []
        for group in contactgroups:
            contactgroup_list.append(group.json_data())

        return HttpResponse(json.dumps(contactgroup_list),
                            content_type="application/json")

    def _post(request):
        try:
            json_data = json.loads(request.body)
            name = json_data["name"]

            new_group, is_new = ContactGroup.objects.get_or_create(name=name)

            response = HttpResponse(json.dumps(new_group.json_data()))
            response.status_code = 201
            return response

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    def _patch(request):
        try:
            json_data = json.loads(request.body)
            contactname = json_data["contact"]
            groupname = json_data["group"]

            group = ContactGroup.objects.get(name=groupname)
            contact = Contact.objects.get(name=contactname)

            group.members.add(contact)

            return HttpResponse("")

        except Exception as ex:
            print "Err: ", ex
            response = HttpResponse(ex)
            response.status_code = 500
            return response

    if request.method == "GET":
        return _get(request)

    if request.method == "POST":
        return _post(request)

    if request.method == "PATCH":
        return _patch(request)


###
#
# Methods supporting the web ui
#
###
def redirect_to_home(request):
    return HttpResponseRedirect(reverse("nagios_registration_home"))


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
        host_data = host.json_data()
        host_data["services"] = []
        host_data["host_groups"] = []

        services = Service.objects.filter(hosts=host)
        for service in services:
            host_data["services"].append(service.json_data())

        groups = HostGroup.objects.filter(hosts=host)
        for group in groups:
            host_data["host_groups"].append(group.json_data())

        host_list.append(host_data)

    return HttpResponse(json.dumps(host_list), content_type="application/json")
