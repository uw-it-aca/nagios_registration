# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nagios_registration', '0002_auto_20141028_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='address',
            field=models.CharField(unique=True, max_length=200, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='name',
            field=models.CharField(unique=True, max_length=200, db_index=True),
            preserve_default=True,
        ),
    ]
