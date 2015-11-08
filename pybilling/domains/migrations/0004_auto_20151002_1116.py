# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('domains', '0003_auto_20151001_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrardomain',
            name='contract',
        ),
        migrations.DeleteModel(
            name='RegistrarDomain',
        ),
    ]
