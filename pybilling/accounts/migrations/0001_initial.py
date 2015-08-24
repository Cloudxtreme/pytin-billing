# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('type', models.CharField(max_length=15, db_index=True)),
                ('default', models.BooleanField(default=False, db_index=True)),
                ('verified', models.BooleanField(default=False, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=155, db_index=True)),
                ('created_at', models.DateTimeField(db_index=True)),
                ('login_at', models.DateTimeField(db_index=True)),
                ('language', models.CharField(default=b'ru', max_length=15, db_index=True)),
                ('resident', models.BooleanField(default=True, db_index=True)),
                ('balance', models.IntegerField(default=0, db_index=True)),
                ('bonus_balance', models.IntegerField(default=0, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('address', models.CharField(max_length=255, db_index=True)),
                ('type', models.CharField(db_index=True, max_length=15, choices=[(b'person', b'person'), (b'entrepreneur', b'entrepreneur'), (b'company', b'company')])),
                ('default', models.BooleanField(default=False, db_index=True)),
                ('verified', models.BooleanField(default=False, db_index=True)),
                ('account', models.ForeignKey(to='accounts.UserAccount')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataCompany',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('country', models.CharField(max_length=55, null=True, db_index=True)),
                ('company_name', models.CharField(max_length=555, null=True, db_index=True)),
                ('company_name_lat', models.CharField(max_length=555, db_index=True)),
                ('inn', models.CharField(max_length=55, null=True, db_index=True)),
                ('ogrn', models.CharField(max_length=55, null=True, db_index=True)),
                ('kpp', models.CharField(max_length=55, null=True, db_index=True)),
                ('postal_person', models.CharField(max_length=355, null=True, db_index=True)),
                ('postal_address', models.CharField(max_length=355, db_index=True)),
                ('postal_index', models.CharField(max_length=35, null=True, db_index=True)),
                ('company_address', models.CharField(max_length=355, db_index=True)),
                ('phone', models.CharField(max_length=55, db_index=True)),
                ('email', models.CharField(max_length=55, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataPerson',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('country', models.CharField(max_length=55, null=True, db_index=True)),
                ('inn_code', models.CharField(max_length=55, null=True, db_index=True)),
                ('fio', models.CharField(max_length=355, null=True, db_index=True)),
                ('fio_lat', models.CharField(max_length=355, db_index=True)),
                ('passport', models.CharField(max_length=555, db_index=True)),
                ('birth', models.DateTimeField(db_index=True)),
                ('postal_address', models.CharField(max_length=355, db_index=True)),
                ('postal_index', models.CharField(max_length=35, null=True, db_index=True)),
                ('phone', models.CharField(max_length=55, db_index=True)),
                ('email', models.CharField(max_length=55, db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='personaldata',
            name='account',
            field=models.ForeignKey(to='accounts.UserAccount'),
        ),
    ]
