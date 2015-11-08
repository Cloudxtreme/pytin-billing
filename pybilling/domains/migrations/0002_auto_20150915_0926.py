# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('domains', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuCenterDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('domain', models.CharField(max_length=155, db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='rucentercontract',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True),
        ),
        migrations.AddField(
            model_name='rucenterdomain',
            name='contract',
            field=models.ForeignKey(to='domains.RuCenterContract'),
        ),
    ]
