# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_airpactuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='airpactuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
