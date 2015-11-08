# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DedicatedServerOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform', models.CharField(max_length=155, db_index=True)),
                ('cpu_name', models.CharField(max_length=155, db_index=True)),
                ('cpu_count', models.PositiveSmallIntegerField(default=1, db_index=True)),
                ('ram_gb', models.PositiveSmallIntegerField(db_index=True)),
                ('hdd_gb', models.PositiveSmallIntegerField(db_index=True)),
                ('hdd_count', models.PositiveSmallIntegerField(default=1, db_index=True)),
                ('price', models.PositiveIntegerField(default=0, db_index=True)),
                ('visible', models.BooleanField(default=False, db_index=True)),
                ('comment', models.TextField(verbose_name='Offer details')),
            ],
        ),
    ]
