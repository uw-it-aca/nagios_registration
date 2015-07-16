from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    address = models.CharField(max_length=200, db_index=True, unique=True)
    contact_groups = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)

    def json_data(self):
        return {
            "name": self.name,
            "address": self.address,
            "contact_groups": self.contact_groups,
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


class ServiceGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    alias = models.CharField(max_length=200)
    services = models.ManyToManyField(Service)

    def json_data(self):
        return {
            "name": self.name,
            "alias": self.alias,
        }


class Contact(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    email = models.CharField(max_length=200, db_index=True, unique=True)

    def json_data(self):
        return {
            "name": self.name,
            "email": self.email,
        }


class ContactGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    members = models.ManyToManyField(Contact)

    def json_data(self):
        return {
            "name": self.name,
        }
