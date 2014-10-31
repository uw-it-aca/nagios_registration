from django.test import TestCase
from django.test.utils import override_settings
from oauth_provider.models import Consumer
from nagios_registration.models import Host, HostGroup, Service
from tempfile import NamedTemporaryFile
import json
import hashlib
import time
import random


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
                                    '{ "name": "T1", "address": "A1" }',
                                    content_type="application/json",
                                    )

        self.assertEquals(response.status_code, 201)

        response = self.client.get("/api/v1/host")
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]["name"], "T1")
        self.assertEquals(data[0]["address"], "A1")

        host = Host.objects.get(name="T1")
        host.delete()

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

        service = Service.objects.get(description="test service")
        self.assertEquals(len(service.hosts.all()), 1)
        self.assertEquals(service.hosts.all()[0].name, "member")

        host.delete()

        service.delete()

    @override_settings(NAGIOS_RESTART_COMMAND="")
    def test_deploy(self):
        f = NamedTemporaryFile()

        with self.settings(NAGIOS_CONFIGURATION_FILE=f.name):
            response = self.client.post("/api/v1/deploy")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.content, "OK")

            file_content = f.read()

            self.assertGreater(len(file_content), 500)
