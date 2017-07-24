# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceModels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_base_path', models.CharField(max_length=30, null=True)),
                ('model_data_path', models.CharField(max_length=30, null=True)),
                ('model_restart_script', models.CharField(max_length=30, null=True)),
                ('model_server_ip', models.ForeignKey(to='asset.Server', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_name', models.CharField(max_length=30, null=True)),
                ('short_name', models.CharField(max_length=10, null=True)),
                ('dev_name', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='servicemodels',
            name='model_service',
            field=models.ForeignKey(to='service.ServiceName', null=True),
        ),
    ]
