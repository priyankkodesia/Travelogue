# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-14 20:38
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('Posts', '0011_auto_20170815_0041'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggedUser',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='post_views',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 15, 2, 8, 41, 13522)),
        ),
    ]
