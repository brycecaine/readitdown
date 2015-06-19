# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('minutes', models.IntegerField()),
                ('pages', models.IntegerField()),
                ('book', models.CharField(max_length=255)),
                ('student', models.ForeignKey(to='default.Student')),
            ],
        ),
    ]
