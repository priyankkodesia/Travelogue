# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-26 17:56
from __future__ import unicode_literals

import Posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0004_auto_20170726_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=Posts.models.upload_location),
        ),
    ]
