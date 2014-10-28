# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nagios_registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='base_service',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='check_command',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='contact_groups',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.CharField(default='', max_length=200, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='hosts',
            field=models.ManyToManyField(to='nagios_registration.Host'),
            preserve_default=True,
        ),
    ]
