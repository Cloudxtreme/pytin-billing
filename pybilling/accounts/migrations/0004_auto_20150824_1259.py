# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150824_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='login_at',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='last_login_at',
            field=models.DateTimeField(null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 24, 12, 59, 0, 317745, tzinfo=utc), db_index=True),
        ),
    ]
