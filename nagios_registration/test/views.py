from django.test import TestCase
from oauth_provider.models import Consumer
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

        valid_response = '[{"name": "T1", "address": "A1"}]'
        self.assertEquals(response.content, valid_response)
