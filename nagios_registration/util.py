from nagios_registration.models import Host, HostGroup, Service, ServiceGroup


def generate_configuration():
    configuration = """
#####
#
#  WRITE-ONLY CONFIGURATION FILE!
#
#  This configuration file was created by nagios_registration.  Any changes
#  made directly to this file will be lost.
#
#####

%s

""" % (get_base_host())

    active_hosts = Host.objects.filter(is_active=True)
    for host in active_hosts:
        configuration += get_host_definition(host)

    hostgroups = HostGroup.objects.all()
    for hostgroup in hostgroups:
        configuration += get_hostgroup_definition(hostgroup)

    for service in Service.objects.all():
        configuration += get_service_definition(service)

    for servicegroup in ServiceGroup.objects.all():
        configuration += get_servicegroup_definition(servicegroup)

    return configuration


def get_service_definition(service):
    if not filter(lambda x: x.is_active, service.hosts.all()):
        return ""
    definition = """
define service {
    use                 %s
    host_name           %s
    service_description %s
    check_command       %s
""" % (
        service.base_service,
        ", ".join(
            map(lambda x: x.name, filter(
                lambda x: x.is_active, service.hosts.all()))),
        service.description,
        service.check_command
        )

    if service.contact_groups:
        definition += "    contact_groups      %s\n" % service.contact_groups

    groups = ServiceGroup.objects.filter(services__id=service.pk)
    if groups:
        name_list = list(map(lambda x: x.name, groups))
        definition += "    servicegroups      %s\n" % (", ".join(name_list))

    definition += """}
"""

    return definition


def get_host_definition(host):
    return """
define host {
    use         _nr_base_host_definition
    host_name   %s
    address     %s
}
""" % (host.name, host.address)


def get_hostgroup_definition(hg):
    if not filter(lambda x: x.is_active, hg.hosts.all()):
        return ""

    return """
define hostgroup {
    hostgroup_name  %s
    alias           %s
    members         %s
}
""" % (
        hg.name,
        hg.alias,
        ", ".join(
            map(lambda x: x.name, filter(
                lambda x: x.is_active, hg.hosts.all()))))


def get_servicegroup_definition(sg):
    if not sg.services.all():
        return ""

    return """
define servicegroup {
    servicegroup_name  %s
    alias           %s
}
""" % (
        sg.name,
        sg.alias,
        )


def get_base_host():
    return """
define host {
    name                            _nr_base_host_definition
    notifications_enabled           1
    event_handler_enabled           1
    flap_detection_enabled          1
    failure_prediction_enabled      1
    process_perf_data               1
    retain_status_information       1
    retain_nonstatus_information    1
    register                        0
    check_command                   check-host-alive
    normal_check_interval           3
    max_check_attempts              5
    notification_interval           120
    notification_period             24x7
    notification_options            d,r,u
    contact_groups                  _nr_default_contacts
}
"""
