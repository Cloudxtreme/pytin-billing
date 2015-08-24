# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalDataEntrepreneur',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('fio', models.CharField(max_length=355, db_index=True)),
                ('fio_lat', models.CharField(max_length=355, db_index=True)),
                ('passport', models.CharField(max_length=555, db_index=True)),
                ('inn_code', models.CharField(max_length=55, db_index=True)),
                ('birth', models.DateTimeField(db_index=True)),
                ('postal_address', models.CharField(max_length=355, db_index=True)),
                ('postal_index', models.CharField(max_length=35, db_index=True)),
                ('phone', models.CharField(max_length=55, db_index=True)),
                ('email', models.CharField(max_length=55, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataForeignCompany',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('country', models.CharField(max_length=55, db_index=True)),
                ('company_name_lat', models.CharField(max_length=555, db_index=True)),
                ('postal_address', models.CharField(max_length=355, db_index=True)),
                ('company_address', models.CharField(max_length=355, db_index=True)),
                ('phone', models.CharField(max_length=55, db_index=True)),
                ('email', models.CharField(max_length=55, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataForeignEntrepreneur',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('country', models.CharField(max_length=55, db_index=True)),
                ('fio_lat', models.CharField(max_length=355, db_index=True)),
                ('passport', models.CharField(max_length=555, db_index=True)),
                ('inn_code', models.CharField(max_length=55, db_index=True)),
                ('birth', models.DateTimeField(db_index=True)),
                ('postal_address', models.CharField(max_length=355, db_index=True)),
                ('phone', models.CharField(max_length=55, db_index=True)),
                ('email', models.CharField(max_length=55, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataForeignPerson',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('country', models.CharField(max_length=55, db_index=True)),
                ('fio_lat', models.CharField(max_length=355, db_index=True)),
                ('passport', models.CharField(max_length=555, db_index=True)),
                ('birth', models.DateTimeField(db_index=True)),
                ('postal_address', models.CharField(max_length=355, db_index=True)),
                ('phone', models.CharField(max_length=55, db_index=True)),
                ('email', models.CharField(max_length=55, db_index=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='personaldatacompany',
            name='country',
        ),
        migrations.RemoveField(
            model_name='personaldataperson',
            name='country',
        ),
        migrations.RemoveField(
            model_name='personaldataperson',
            name='inn_code',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='resident',
        ),
        migrations.AlterField(
            model_name='personaldata',
            name='type',
            field=models.CharField(db_index=True, max_length=15, choices=[(b'person', b'person'), (b'entrepreneur', b'entrepreneur'), (b'company', b'company')]),
        ),
        migrations.AlterField(
            model_name='personaldatacompany',
            name='company_name',
            field=models.CharField(default='', max_length=555, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personaldatacompany',
            name='inn',
            field=models.CharField(default='', max_length=55, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personaldatacompany',
            name='kpp',
            field=models.CharField(default='', max_length=55, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personaldatacompany',
            name='postal_index',
            field=models.CharField(default='', max_length=35, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personaldatacompany',
            name='postal_person',
            field=models.CharField(default='', max_length=355, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personaldataperson',
            name='fio',
            field=models.CharField(default='', max_length=355, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personaldataperson',
            name='postal_index',
            field=models.CharField(default='', max_length=35, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usercontact',
            name='type',
            field=models.CharField(max_length=15, db_index=True),
        ),
    ]
