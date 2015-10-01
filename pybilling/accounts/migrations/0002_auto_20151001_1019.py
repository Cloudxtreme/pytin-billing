# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldatacompany',
            name='inn',
            field=models.CharField(max_length=10, db_index=True),
        ),
        migrations.AlterField(
            model_name='personaldatacompany',
            name='kpp',
            field=models.CharField(max_length=9, db_index=True),
        ),
        migrations.AlterField(
            model_name='personaldatacompany',
            name='ogrn',
            field=models.CharField(max_length=13, null=True, db_index=True),
        ),
    ]
