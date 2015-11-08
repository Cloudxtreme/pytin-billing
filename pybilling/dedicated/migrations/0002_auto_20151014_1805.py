# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dedicated', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dedicatedserveroffer',
            name='comment',
            field=models.TextField(verbose_name='Offer details', blank=True),
        ),
    ]
