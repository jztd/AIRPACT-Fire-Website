# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0009_auto_20161027_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='algorithmType',
            field=models.TextField(default='uknown', null=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='objectSkyVr',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='description',
            field=models.TextField(default=' ', null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='uploaded',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
