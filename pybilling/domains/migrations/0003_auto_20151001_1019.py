# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_auto_20151001_1019'),
        ('domains', '0002_auto_20150915_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrarContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('registrar', models.CharField(max_length=35, db_index=True)),
                ('number', models.CharField(max_length=15, db_index=True)),
                ('personal_data', models.ForeignKey(to='accounts.PersonalData')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrarDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('domain', models.CharField(max_length=155, db_index=True)),
                ('contract', models.ForeignKey(to='domains.RegistrarContract')),
            ],
        ),
        migrations.RemoveField(
            model_name='rucentercontract',
            name='personal_data',
        ),
        migrations.RemoveField(
            model_name='rucenterdomain',
            name='contract',
        ),
        migrations.DeleteModel(
            name='RuCenterContract',
        ),
        migrations.DeleteModel(
            name='RuCenterDomain',
        ),
    ]
