# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import userapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0005_profile_pro_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pro_photo',
            field=models.ImageField(upload_to=userapp.models.upload_to),
            preserve_default=True,
        ),
    ]
