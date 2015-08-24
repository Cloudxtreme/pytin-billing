# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150824_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaldata',
            name='name',
        ),
        migrations.AlterField(
            model_name='personaldata',
            name='type',
            field=models.CharField(max_length=15, db_index=True),
        ),
    ]
