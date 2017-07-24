# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_service_script'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='script',
            field=models.IntegerField(max_length=20, null=True, choices=[(1, b'java_core_restart.sh'), (2, b'tomcat_restart.sh'), (3, b'nginx_restart.sh'), (4, b'php_restart.sh'), (5, b'fastdfs_restart.sh'), (6, b'redis_restart.sh')]),
        ),
    ]
