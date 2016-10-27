# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0008_auto_20161020_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='farTargetDistance',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='nearTargetDistance',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='vrUnits',
            field=models.CharField(default='K', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(upload_to='pictures/'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='pictureWithCircles',
            field=models.ImageField(null=True, upload_to='circles/', blank=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='thumbnails/', blank=True),
        ),
    ]
