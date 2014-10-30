# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nagios_registration', '0004_auto_20141030_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(unique=True, max_length=200, db_index=True),
            preserve_default=True,
        ),
    ]
