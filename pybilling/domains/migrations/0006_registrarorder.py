# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0005_auto_20151008_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrarOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('domain', models.CharField(max_length=255, db_index=True)),
                ('is_prolong', models.BooleanField(default=False)),
                ('prolong_years', models.IntegerField(default=0)),
                ('contract', models.ForeignKey(to='domains.RegistrarContract')),
            ],
        ),
    ]
