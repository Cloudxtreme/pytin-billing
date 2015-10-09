# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from domains.models import RegistrarContract


def remove_duplicates(apps, schema_editor):
    for reg_contract in RegistrarContract.objects.all():
        for local_contract in RegistrarContract.objects.filter(personal_data=reg_contract.personal_data)[1:]:
            local_contract.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('domains', '0004_auto_20151002_1116'),
    ]

    operations = [
        migrations.RunPython(remove_duplicates),
        migrations.RemoveField(
            model_name='registrarcontract',
            name='id',
        ),
        migrations.AlterField(
            model_name='registrarcontract',
            name='personal_data',
            field=models.OneToOneField(primary_key=True, serialize=False, to='accounts.PersonalData'),
        ),
    ]
