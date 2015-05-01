# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostInteract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view_count', models.IntegerField(default=0)),
                ('share_count', models.IntegerField(default=0)),
                ('contact_count', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='postinteract',
            field=models.OneToOneField(null=True, to='app_post.PostInteract'),
            preserve_default=True,
        ),
    ]
