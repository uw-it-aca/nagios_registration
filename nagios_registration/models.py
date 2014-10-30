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
    name = models.CharField(max_length=200, db_index=True)
    alias = models.CharField(max_length=200)
    hosts = models.ManyToManyField(Host)


class Service(models.Model):
    base_service = models.CharField(max_length=200)
    description = models.CharField(max_length=200, db_index=True)
    contact_groups = models.CharField(max_length=200, null=True)
    hosts = models.ManyToManyField(Host)
    check_command = models.CharField(max_length=500)
