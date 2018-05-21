import oauth2
import json

###
#
# This script will create 2 hosts, and add them to a host group.
# It will then create a service, and assign that service to both hosts.
# It will then deploy a new nagios configuration file.
#
###

consumer_key = "OAUTH_KEY"
consumer_secret = "OAUTH_SECRET"

registration_server = "http://localhost:8000"

###
#
# You can create a consumer key and secret on the nagios_registration
# server with a django management command:
#
# python manage.py create_consumer
#
###


consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
client = oauth2.Client(consumer)

# Variables used by the actual requests below

hostname1 = "example app host"
address1 = "127.0.0.1"

hostname2 = "second app host"
address2 = "127.0.0.2"

groupname = "example_app_servers"
alias = "Example App Servers"

base_service = "24x7-active-service"
service_description = "Disk Usage"
check_command = "check_remote!disk_check.py!98!99"

# End of settings, now just making requests to the server

# Create the 2 hosts
client.request("%s/api/v1/host" % (registration_server),
               method='POST',
               body=json.dumps({"name": hostname1, "address": address1, "contact_groups": ""}),
               headers={"Content-Type": "application/json"})

client.request("%s/api/v1/host" % (registration_server),
               method='POST',
               body=json.dumps({"name": hostname2, "address": address2, "contact_groups": ""}),
               headers={"Content-Type": "application/json"})

# Create the hostgroup
client.request("%s/api/v1/hostgroup" % (registration_server),
               method='POST',
               body=json.dumps({"name": groupname, "alias": alias}),
               headers={"Content-Type": "application/json"})

# Add the hosts to the hostgroup
client.request("%s/api/v1/hostgroup" % (registration_server),
               method='PATCH',
               body=json.dumps({"group": groupname, "host": hostname1}),
               headers={"Content-Type": "application/json"})

client.request("%s/api/v1/hostgroup" % (registration_server),
               method='PATCH',
               body=json.dumps({"group": groupname, "host": hostname2}),
               headers={"Content-Type": "application/json"})

# Create a service
client.request("%s/api/v1/service" % (registration_server),
               method='POST',
               body=json.dumps({"base_service": base_service,
                                "description": service_description,
                                "check_command": check_command}),
               headers={"Content-Type": "application/json"})

# Add the service to the 2 hosts
client.request("%s/api/v1/service" % (registration_server),
               method='PATCH',
               body=json.dumps({"service": service_description,
                                "host": hostname1}),
               headers={"Content-Type": "application/json"})

client.request("%s/api/v1/service" % (registration_server),
               method='PATCH',
               body=json.dumps({"service": service_description,
                                "host": hostname2}),
               headers={"Content-Type": "application/json"})

# Deploy the changes
client.request("%s/api/v1/deploy" % (registration_server), method="POST")

print "Done!"
