# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0007_auto_20160926_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='twoTargetContrastVr',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(upload_to='media/pictures/'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='pictureWithCircles',
            field=models.ImageField(null=True, upload_to='media/circles/', blank=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='media/thumbnails/', blank=True),
        ),
    ]
