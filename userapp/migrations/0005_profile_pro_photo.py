# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_auto_20150206_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pro_photo',
            field=models.ImageField(default='nobody.jpg', upload_to=b''),
            preserve_default=False,
        ),
    ]
