# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_summernote.fields
import app_class.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_summernote', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassDetail',
            fields=[
                ('attachment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_summernote.Attachment')),
                ('class_detail', django_summernote.fields.SummernoteTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=('django_summernote.attachment',),
        ),
        migrations.CreateModel(
            name='ClassPic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_photo', models.ImageField(null=True, upload_to=app_class.models.upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=120)),
                ('title', models.CharField(max_length=150)),
                ('price', models.IntegerField()),
                ('describe', models.TextField(max_length=500)),
                ('lessonday', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('minimum', models.IntegerField()),
                ('maximum', models.IntegerField()),
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
            model_name='classpic',
            name='class_post',
            field=models.ForeignKey(to='app_class.ClassPost'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classpic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classdetail',
            name='class_post',
            field=models.ForeignKey(to='app_class.ClassPost'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classdetail',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
