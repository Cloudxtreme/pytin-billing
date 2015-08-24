# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150824_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldata',
            name='type',
            field=models.CharField(max_length=55, db_index=True),
        ),
    ]
