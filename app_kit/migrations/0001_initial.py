# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_summernote.fields
import app_kit.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_summernote', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kit_Detailm',
            fields=[
                ('attachment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_summernote.Attachment')),
                ('kit_detail', django_summernote.fields.SummernoteTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=('django_summernote.attachment',),
        ),
        migrations.CreateModel(
            name='Kit_Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kit_photo', models.ImageField(null=True, upload_to=app_kit.models.upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kit_Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=120)),
                ('title', models.CharField(max_length=150)),
                ('price', models.IntegerField()),
                ('describe', models.TextField(max_length=500)),
                ('contact_tel', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='kit_photo',
            name='kit_post',
            field=models.ForeignKey(to='app_kit.Kit_Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kit_photo',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kit_detailm',
            name='kit_post',
            field=models.ForeignKey(to='app_kit.Kit_Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kit_detailm',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
