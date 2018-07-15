# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='priority',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='thing',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
