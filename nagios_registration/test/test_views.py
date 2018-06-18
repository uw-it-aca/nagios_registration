from django.test import TestCase
from django.test.utils import override_settings
from oauth_provider.models import Consumer
from nagios_registration.models import Host, HostGroup, Service, ServiceGroup
from nagios_registration.models import Contact, ContactGroup
from tempfile import NamedTemporaryFile
import json
import hashlib
import time
import random
import urllib


class TestViews(TestCase):
    def setUp(self):
        consumer_name = "Test client"
        key = hashlib.sha1("{0} - {1}".format(random.random(),
                                              time.time())).hexdigest()
        secret = hashlib.sha1("{0} - {1}".format(random.random(),
                                                 time.time())).hexdigest()
        consumer = Consumer.objects.create(name=consumer_name,
                                           key=key,
                                           secret=secret)

        header = 'OAuth oauth_version="1.0", oauth_signature_method="' +\
                 'PLAINTEXT", oauth_nonce="requestnonce", oauth_timestamp=' +\
                 '"%s", oauth_consumer_key="%s", oauth_signature="%s&' \
                 % (str(int(time.time())), key, secret)
        self.client.defaults['Authorization'] = header

    def test_hosts(self):
        response = self.client.get("/api/v1/host")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

        response = self.client.post("/api/v1/host",
                                    ('{ "name": "T1", "address": "A1", '
                                     '"contact_groups": "cg1, cg2" }'),
                                    content_type="application/json",
                                    )

        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/host")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["name"], "T1")
        self.assertEquals(data[0]["address"], "A1")
        self.assertEquals(data[0]["contact_groups"], "cg1, cg2")

        response = self.client.post("/api/v1/host",
                                    ('{ "name": "T1", "address": "A1", '
                                     '"contact_groups": "cg1" }'),
                                    content_type="application/json",
                                    )

        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/host")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["name"], "T1")
        self.assertEquals(data[0]["address"], "A1")
        self.assertEquals(data[0]["contact_groups"], "cg1")

        host = Host.objects.get(name="T1")
        host.delete()

    def test_delete_host(self):
        response = self.client.get("/api/v1/host")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

        response = self.client.post("/api/v1/host",
                                    ('{ "name": "T1", "address": "A1", '
                                     '"contact_groups": "cg1, cg2" }'),
                                    content_type="application/json",
                                    )
        self.assertEquals(response.status_code, 201)
        response = self.client.post("/api/v1/host",
                                    ('{ "name": "T 1", "address": "A2", '
                                     '"contact_groups": "cg1, cg2" }'),
                                    content_type="application/json",
                                    )
        self.assertEquals(response.status_code, 201)

        # Delete a host with a space in its name
        response = self.client.delete("/api/v1/host/T 1")

        response = self.client.get("/api/v1/host")
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)

        # Delete the other one too
        response = self.client.delete("/api/v1/host/T1")

        response = self.client.get("/api/v1/host")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

    def test_delete_host_deletes_service(self):
        response = self.client.get("/api/v1/host")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

        response = self.client.post("/api/v1/host",
                                    ('{ "name": "T1", "address": "A1", '
                                     '"contact_groups": "cg1, cg2" }'),
                                    content_type="application/json",
                                    )
        self.assertEquals(response.status_code, 201)

        response = self.client.post("/api/v1/service",
                                    json.dumps({
                                         "base_service": "24x7",
                                         "description": "test service",
                                         "check_command": "!!something.py!80",
                                         "contact_groups": "admins, yousall",
                                     }),
                                    content_type="application/json",
                                    )
        self.assertEquals(response.status_code, 201)

        response = self.client.patch("/api/v1/service",
                                     json.dumps({"service": "test service",
                                                 "host": "T1",
                                                 }))
        self.assertEquals(response.status_code, 200)
        response = self.client.get("/api/v1/service")
        self.assertEquals(response.status_code, 200)

        # Assert that the service is connected to the host
        host = Host.objects.filter(name="T1")
        services = Service.objects.filter(hosts=host)
        self.assertEquals(len(services.all()), 1)

        # Delete the host, now no more services should be attached to the host
        response = self.client.delete("/api/v1/host/T1")
        services = Service.objects.filter(hosts=host)
        self.assertEquals(len(services.all()), 0)

        # However, the service should still exist
        services = Service.objects.all()
        self.assertEquals(len(services.all()), 1)

        service = Service.objects.get(description="test service")
        service.delete()

    def test_host_group(self):
        response = self.client.get("/api/v1/hostgroup")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

        response = self.client.post("/api/v1/hostgroup",
                                    '{ "name": "HG1", "alias": "HG1_alias" }',
                                    content_type="application/json",
                                    )

        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/hostgroup")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["name"], "HG1")
        self.assertEquals(data[0]["alias"], "HG1_alias")

        host = Host.objects.create(name="member", address="address")

        response = self.client.patch("/api/v1/hostgroup",
                                     '{ "group": "HG1", "host": "member" }')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "")

        hostgroup = HostGroup.objects.get(name="HG1")
        self.assertEquals(len(hostgroup.hosts.all()), 1)
        self.assertEquals(hostgroup.hosts.all()[0].name, "member")

        host.delete()

        hostgroup.delete()

    def test_service(self):
        response = self.client.get("/api/v1/service")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

        response = self.client.post("/api/v1/service",
                                    json.dumps({
                                        "base_service": "24x7",
                                        "description": "test service",
                                        "check_command": "!!something.py!80",
                                        "contact_groups": "admins, yousall",
                                    }),
                                    content_type="application/json",
                                    )

        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/service")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["base_service"], "24x7")
        self.assertEquals(data[0]["description"], "test service")
        self.assertEquals(data[0]["check_command"], "!!something.py!80")
        self.assertEquals(data[0]["contact_groups"], "admins, yousall")

        host = Host.objects.create(name="member", address="address")

        response = self.client.patch("/api/v1/service",
                                     json.dumps({"service": "test service",
                                                 "host": "member",
                                                 }))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "")

        response = self.client.patch("/api/v1/service", "bad_data")

        self.assertEquals(response.status_code, 500)

        service = Service.objects.get(description="test service")
        self.assertEquals(len(service.hosts.all()), 1)
        self.assertEquals(service.hosts.all()[0].name, "member")

        # Test POSTing a different check_command/contact_groups/base_service
        response = self.client.post("/api/v1/service",
                                    json.dumps({
                                        "base_service": "25x8",
                                        "description": "test service",
                                        "check_command": "!!something.py!90",
                                        "contact_groups": "admins",
                                    }),
                                    content_type="application/json",
                                    )
        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/service")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["base_service"], "25x8")
        self.assertEquals(data[0]["description"], "test service")
        self.assertEquals(data[0]["check_command"], "!!something.py!90")
        self.assertEquals(data[0]["contact_groups"], "admins")

        host.delete()

        service.delete()

    def test_delete_service(self):
        host = Host.objects.create(name="T1", address="address")
        service_name = "~test/sample.py"
        response = self.client.post("/api/v1/service",
                                    json.dumps({
                                        "base_service": "24x7",
                                        "description": service_name,
                                        "check_command": "!!something.py!80",
                                        "contact_groups": "admins, yousall",
                                    }),
                                    content_type="application/json",
                                    )
        self.assertEquals(response.status_code, 201)
        services = Service.objects.filter(hosts=host)
        self.assertEquals(len(services.all()), 0)

        response = self.client.patch("/api/v1/service",
                                     json.dumps({"service": service_name,
                                                 "host": "T1",
                                                 }))
        self.assertEquals(response.status_code, 200)
        services = Service.objects.filter(hosts=host)
        self.assertEquals(len(services.all()), 1)

        api = "/api/v1/service/T1/" + urllib.quote(service_name, safe='')
        response = self.client.delete(api)
        self.assertEquals(response.status_code, 200)

        # Assert that the service is not connected to host
        services = Service.objects.filter(hosts=host)
        self.assertEquals(len(services.all()), 0)

        # Assert that the service still exists...
        service = Service.objects.filter(description=service_name)
        self.assertEquals(len(service.all()), 1)

        host.delete()
        service.delete()

    def test_contact(self):
        response = self.client.get("/api/v1/contact")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

        response = self.client.post("/api/v1/contact",
                                    json.dumps({
                                        "name": "contact_rest",
                                        "email": "cr@example.com",
                                    }),
                                    content_type="application/json",
                                    )

        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/contact")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["name"], "contact_rest")
        self.assertEquals(data[0]["email"], "cr@example.com")

        contact = Contact.objects.get(name="contact_rest")
        contact.delete()

    def test_service_group(self):
        response = self.client.get("/api/v1/servicegroup")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

        response = self.client.post("/api/v1/servicegroup",
                                    '{ "name": "SG1", "alias": "SG1_alias" }',
                                    content_type="application/json",
                                    )

        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/servicegroup")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["name"], "SG1")
        self.assertEquals(data[0]["alias"], "SG1_alias")

        service = Service.objects.create(description="smember",
                                         base_service="base_service",
                                         check_command="okok")

        response = self.client.patch("/api/v1/servicegroup",
                                     ('{ "group": "SG1", '
                                      '"service": "smember" }'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "")

        servicegroup = ServiceGroup.objects.get(name="SG1")
        self.assertEquals(len(servicegroup.services.all()), 1)
        self.assertEquals(servicegroup.services.all()[0].description,
                          "smember")

        service.delete()

        servicegroup.delete()

    def test_contact_group(self):
        response = self.client.get("/api/v1/contactgroup")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

        response = self.client.post("/api/v1/contactgroup",
                                    '{ "name": "CG1" }',
                                    content_type="application/json",
                                    )

        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/contactgroup")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["name"], "CG1")

        contact = Contact.objects.create(name="cmember",
                                         email="xm@example.com",
                                         )

        response = self.client.patch("/api/v1/contactgroup",
                                     ('{ "group": "CG1", '
                                      '"contact": "cmember" }'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "")

        contactgroup = ContactGroup.objects.get(name="CG1")
        self.assertEquals(len(contactgroup.members.all()), 1)
        self.assertEquals(contactgroup.members.all()[0].name,
                          "cmember")

        contact.delete()

        contactgroup.delete()

    @override_settings(NAGIOS_RESTART_COMMAND="")
    def test_deploy(self):
        f = NamedTemporaryFile()

        with self.settings(NAGIOS_CONFIGURATION_FILE=f.name):
            response = self.client.post("/api/v1/deploy")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.content, "OK")

            file_content = f.read()

            self.assertGreater(len(file_content), 500)
