# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-22 05:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0005_auto_20160428_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='static/thumbnails/'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(upload_to='static/pictures/'),
        ),
    ]
