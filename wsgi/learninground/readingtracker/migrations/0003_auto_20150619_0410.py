# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readingtracker', '0002_auto_20150619_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='book',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='pages',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
