# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_airpactuser_bob'),
    ]

    operations = [
        migrations.AddField(
            model_name='airpactuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
