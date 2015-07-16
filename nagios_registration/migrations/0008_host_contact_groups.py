# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nagios_registration', '0007_contact_contactgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='contact_groups',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
