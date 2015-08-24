# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150824_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldatacompany',
            name='company_name',
            field=models.CharField(max_length=355, db_index=True),
        ),
        migrations.AlterField(
            model_name='personaldatacompany',
            name='company_name_lat',
            field=models.CharField(max_length=555),
        ),
        migrations.AlterField(
            model_name='personaldataentrepreneur',
            name='passport',
            field=models.CharField(max_length=555),
        ),
        migrations.AlterField(
            model_name='personaldataforeigncompany',
            name='company_address',
            field=models.CharField(max_length=355),
        ),
        migrations.AlterField(
            model_name='personaldataforeigncompany',
            name='company_name_lat',
            field=models.CharField(max_length=355, db_index=True),
        ),
        migrations.AlterField(
            model_name='personaldataforeigncompany',
            name='postal_address',
            field=models.CharField(max_length=355),
        ),
        migrations.AlterField(
            model_name='personaldataforeignentrepreneur',
            name='passport',
            field=models.CharField(max_length=555),
        ),
        migrations.AlterField(
            model_name='personaldataforeignperson',
            name='passport',
            field=models.CharField(max_length=555),
        ),
        migrations.AlterField(
            model_name='personaldataperson',
            name='passport',
            field=models.CharField(max_length=555),
        ),
    ]
