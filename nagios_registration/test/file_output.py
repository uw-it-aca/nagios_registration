from django.test import TestCase
from nagios_registration.util import generate_configuration, get_base_host
from nagios_registration.models import Host, HostGroup, Service, ServiceGroup


class TestFile(TestCase):
    def test_baseline(self):
        self.assertRegexpMatches(generate_configuration(), r"WRITE-ONLY")

    def test_host_definition(self):
        host = Host.objects.create(
            is_active=True,
            name="find_me",
            address="127.7.2.1")

        self.assertRegexpMatches(
            generate_configuration(),
            r"host_name\s+find_me\s+address\s+127.7.2.1")

        host.is_active = False
        host.save()
        self.assertNotRegexpMatches(
            generate_configuration(),
            r"host_name\s+find_me\s+address\s+127.7.2.1")

        host.is_active = True
        host.save()
        host.delete()
        self.assertNotRegexpMatches(
            generate_configuration(),
            r"host_name\s+find_me\s+address\s+127.7.2.1")

    def test_hostgroups_definition(self):
        host1 = Host.objects.create(is_active=True, name="f1", address="a1")
        host2 = Host.objects.create(is_active=True, name="f2", address="a2")
        host3 = Host.objects.create(is_active=True, name="f3", address="a3")

        group1 = HostGroup.objects.create(name="hg1", alias="test group 1")
        group2 = HostGroup.objects.create(name="hg2", alias="test group 2")

        group1.hosts.add(host1, host2)
        group2.hosts.add(host2, host3)

        self.assertRegexpMatches(
            generate_configuration(),
            r"hostgroup_name\s+hg1\s+alias\s+test group 1\s+members\s+f1, f2")

        host1.is_active = False
        host1.save()
        self.assertRegexpMatches(
            generate_configuration(),
            r"hostgroup_name\s+hg1\s+alias\s+test group 1\s+members\s+f2")

        host2.is_active = False
        host2.save()
        self.assertNotRegexpMatches(
            generate_configuration(),
            r"hostgroup_name\s+hg1")

        host1.delete()
        host2.delete()
        host3.delete()

        group1.delete()
        group2.delete()

    def test_service_definition(self):
        host1 = Host.objects.create(is_active=True, name="f1", address="a1")
        host2 = Host.objects.create(is_active=True, name="f2", address="a2")

        service = Service.objects.create(base_service="active-service",
                                         description="Disk Usage",
                                         check_command="check.pl!5!8"
                                         )

        service.hosts.add(host1, host2)

        self.assertRegexpMatches(
            generate_configuration(),
            r"service {\s+use\s+active-service\s+host_name\s+f1, f2")

        self.assertRegexpMatches(
            generate_configuration(),
            r"service {[^}]+service_description\s+Disk Usage")

        self.assertRegexpMatches(
            generate_configuration(),
            r"service {[^}]+check_command\s+check.pl!5!8")

        self.assertNotRegexpMatches(
            generate_configuration(),
            r"service {[^}]+contact_groups\s+")

        service.contact_groups = "custom_recipients"
        service.save()

        self.assertRegexpMatches(
            generate_configuration(),
            r"service {[^}]+contact_groups\s+custom_recipients")

        host1.is_active = False
        host1.save()

        self.assertNotRegexpMatches(
            generate_configuration(),
            r"service {\s+use\s+active-service\s+host_name\s+f1, f2")

        self.assertRegexpMatches(
            generate_configuration(),
            r"service {\s+use\s+active-service\s+host_name\s+f2")

        host2.is_active = False
        host2.save()
        self.assertNotRegexpMatches(
            generate_configuration(),
            r"service {\s+use\s+active-service\s+host_name\s")

        host1.delete()
        host2.delete()
        service.delete()

    def test_servicegroups(self):
        host1 = Host.objects.create(is_active=True, name="f1", address="a1")
        host2 = Host.objects.create(is_active=True, name="f2", address="a2")

        service = Service.objects.create(base_service="active-service",
                                         description="Disk Usage",
                                         check_command="check.pl!5!8"
                                         )

        service.hosts.add(host1, host2)

        group1 = ServiceGroup.objects.create(name="disk",
                                             alias="Disk Services")

        group2 = ServiceGroup.objects.create(name="disk2",
                                             alias="Disk Services (2)")


        group1.services.add(service)
        group2.services.add(service)

        config = generate_configuration()

        self.assertRegexpMatches(
            config,
            r"servicegroup {\s+servicegroup_name\s+disk2")

        self.assertRegexpMatches(
            config,
            r"servicegroups\s+disk, disk2")
