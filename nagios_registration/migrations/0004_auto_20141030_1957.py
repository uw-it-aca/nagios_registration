# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nagios_registration', '0003_auto_20141030_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostgroup',
            name='name',
            field=models.CharField(unique=True, max_length=200, db_index=True),
            preserve_default=True,
        ),
    ]
