# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20170721_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_name',
            field=models.CharField(max_length=30, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='short_name',
            field=models.CharField(max_length=10, unique=True, null=True),
        ),
    ]
