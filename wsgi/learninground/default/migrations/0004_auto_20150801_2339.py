# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendship',
            name='is_parent',
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend_type',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
