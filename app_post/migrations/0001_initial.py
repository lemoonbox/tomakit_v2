# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_summernote.fields
import app_post.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_summernote', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('price', models.IntegerField(null=True)),
                ('describe', models.TextField(max_length=500)),
                ('lessonday', models.DateField(null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('minimum', models.IntegerField(null=True)),
                ('maximum', models.IntegerField(null=True)),
                ('contact_tel', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostDetail',
            fields=[
                ('attachment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_summernote.Attachment')),
                ('post_detail', django_summernote.fields.SummernoteTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ManyToManyField(to='app_post.PostCategory')),
                ('post', models.ForeignKey(to='app_post.Post')),
            ],
            options={
            },
            bases=('django_summernote.attachment',),
        ),
        migrations.CreateModel(
            name='PostPic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_photo', models.ImageField(null=True, upload_to=app_post.models.upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ManyToManyField(to='app_post.PostCategory')),
                ('post', models.ForeignKey(to='app_post.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='postpic',
            name='type',
            field=models.ForeignKey(to='app_post.PostType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postpic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postdetail',
            name='type',
            field=models.ForeignKey(to='app_post.PostType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postdetail',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(to='app_post.PostCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.ForeignKey(to='app_post.PostType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
