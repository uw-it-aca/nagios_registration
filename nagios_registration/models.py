from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    address = models.CharField(max_length=200, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    def json_data(self):
        return {
            "name": self.name,
            "address": self.address,
        }


class HostGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    alias = models.CharField(max_length=200)
    hosts = models.ManyToManyField(Host)

    def json_data(self):
        return {
            "name": self.name,
            "alias": self.alias,
        }


class Service(models.Model):
    base_service = models.CharField(max_length=200)
    description = models.CharField(max_length=200, db_index=True, unique=True)
    contact_groups = models.CharField(max_length=200, null=True)
    hosts = models.ManyToManyField(Host)
    check_command = models.CharField(max_length=500)

    def json_data(self):
        return {
            "base_service": self.base_service,
            "description": self.description,
            "contact_groups": self.contact_groups,
            "check_command": self.check_command,
        }
