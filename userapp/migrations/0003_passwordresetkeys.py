# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_auto_20150201_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetKeys',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='userapp.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
