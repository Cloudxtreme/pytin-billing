# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuCenterContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'NIC-D', max_length=15, db_index=True,
                                          choices=[(b'NIC-A', 'Information partner'), (b'NIC-D', 'Regular customer'),
                                                   (b'NIC-REG', 'Resell domains')])),
                ('verified', models.BooleanField(default=False, db_index=True)),
                ('personal_data', models.ForeignKey(to='accounts.PersonalData')),
            ],
        ),
    ]
