# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=55, db_index=True)),
                ('default', models.BooleanField(default=False, db_index=True)),
                ('verified', models.BooleanField(default=False, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=155, db_index=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('last_login_at', models.DateTimeField(null=True, db_index=True)),
                ('language', models.CharField(default='ru', max_length=15, db_index=True)),
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
                ('type', models.CharField(max_length=15, db_index=True)),
                ('default', models.BooleanField(default=False, db_index=True)),
                ('verified', models.BooleanField(default=False, db_index=True)),
                ('account', models.ForeignKey(to='accounts.UserAccount')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataCompany',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('company_name', models.CharField(max_length=255, db_index=True)),
                ('company_name_lat', models.CharField(db_index=True, max_length=255, blank=True)),
                ('inn', models.CharField(max_length=55, db_index=True)),
                ('ogrn', models.CharField(max_length=55, null=True, db_index=True)),
                ('kpp', models.CharField(max_length=55, db_index=True)),
                ('postal_person', models.CharField(max_length=255, db_index=True)),
                ('postal_address', models.CharField(max_length=255, db_index=True)),
                ('postal_index', models.CharField(max_length=35, db_index=True)),
                ('company_address', models.CharField(max_length=255, db_index=True)),
                ('phone', models.CharField(db_index=True, max_length=55, validators=[
                    django.core.validators.RegexValidator(re.compile('^\\+\\d+\\s+\\d{3}\\s+\\d+\\Z'),
                                                          'Phone format is +#[#] ### #######', 'invalid')])),
                ('email',
                 models.CharField(db_index=True, max_length=55, validators=[django.core.validators.EmailValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataEntrepreneur',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('fio', models.CharField(max_length=255, db_index=True)),
                ('fio_lat', models.CharField(db_index=True, max_length=255, blank=True)),
                ('passport', models.CharField(max_length=555)),
                ('inn_code', models.CharField(max_length=55, db_index=True)),
                ('birth', models.DateTimeField(db_index=True)),
                ('postal_address', models.CharField(max_length=255, db_index=True)),
                ('postal_index', models.CharField(max_length=35, db_index=True)),
                ('phone', models.CharField(db_index=True, max_length=55, validators=[
                    django.core.validators.RegexValidator(re.compile('^\\+\\d+\\s+\\d{3}\\s+\\d+\\Z'),
                                                          'Phone format is +#[#] ### #######', 'invalid')])),
                ('email',
                 models.CharField(db_index=True, max_length=55, validators=[django.core.validators.EmailValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataForeignCompany',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('country', models.CharField(max_length=55, db_index=True)),
                ('company_name_lat', models.CharField(max_length=255, db_index=True)),
                ('postal_address', models.CharField(max_length=255)),
                ('company_address', models.CharField(max_length=255)),
                ('phone', models.CharField(db_index=True, max_length=55, validators=[
                    django.core.validators.RegexValidator(re.compile('^\\+\\d+\\s+\\d{3}\\s+\\d+\\Z'),
                                                          'Phone format is +#[#] ### #######', 'invalid')])),
                ('email',
                 models.CharField(db_index=True, max_length=55, validators=[django.core.validators.EmailValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataForeignEntrepreneur',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('country', models.CharField(max_length=55, db_index=True)),
                ('fio_lat', models.CharField(max_length=255, db_index=True)),
                ('passport', models.CharField(max_length=255, db_index=True)),
                ('inn_code', models.CharField(max_length=55, db_index=True)),
                ('birth', models.DateTimeField(db_index=True)),
                ('postal_address', models.CharField(max_length=255, db_index=True)),
                ('phone', models.CharField(db_index=True, max_length=55, validators=[
                    django.core.validators.RegexValidator(re.compile('^\\+\\d+\\s+\\d{3}\\s+\\d+\\Z'),
                                                          'Phone format is +#[#] ### #######', 'invalid')])),
                ('email',
                 models.CharField(db_index=True, max_length=55, validators=[django.core.validators.EmailValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataForeignPerson',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('country', models.CharField(max_length=55, db_index=True)),
                ('fio_lat', models.CharField(max_length=255, db_index=True)),
                ('passport', models.CharField(max_length=255, db_index=True)),
                ('birth', models.DateTimeField(db_index=True)),
                ('postal_address', models.CharField(max_length=255, db_index=True)),
                ('phone', models.CharField(db_index=True, max_length=55, validators=[
                    django.core.validators.RegexValidator(re.compile('^\\+\\d+\\s+\\d{3}\\s+\\d+\\Z'),
                                                          'Phone format is +#[#] ### #######', 'invalid')])),
                ('email',
                 models.CharField(db_index=True, max_length=55, validators=[django.core.validators.EmailValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDataPerson',
            fields=[
                ('common_data', models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData')),
                ('fio', models.CharField(max_length=255, db_index=True)),
                ('fio_lat', models.CharField(db_index=True, max_length=255, blank=True)),
                ('passport', models.CharField(max_length=555)),
                ('birth', models.DateTimeField(db_index=True)),
                ('postal_address', models.CharField(max_length=255, db_index=True)),
                ('postal_index', models.CharField(max_length=35, db_index=True)),
                ('phone', models.CharField(db_index=True, max_length=55, validators=[
                    django.core.validators.RegexValidator(re.compile('^\\+\\d+\\s+\\d{3}\\s+\\d+\\Z'),
                                                          'Phone format is +#[#] ### #######', 'invalid')])),
                ('email',
                 models.CharField(db_index=True, max_length=55, validators=[django.core.validators.EmailValidator()])),
            ],
        ),
        migrations.AddField(
            model_name='personaldata',
            name='account',
            field=models.ForeignKey(to='accounts.UserAccount'),
        ),
    ]
