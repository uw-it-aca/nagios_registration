from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    address = models.CharField(max_length=200, db_index=True)
    is_active = models.BooleanField(default=True)


class HostGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    alias = models.CharField(max_length=200)
    hosts = models.ManyToManyField(Host)

class Service(models.Model):
    pass
