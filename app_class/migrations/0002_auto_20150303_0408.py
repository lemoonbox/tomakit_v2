# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_class', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classpost',
            old_name='phone_tel',
            new_name='contact_tel',
        ),
        migrations.RemoveField(
            model_name='classpost',
            name='store_tel',
        ),
    ]
