# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('readingtracker', '0002_auto_20150619_0337'),
        ('default', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.NullBooleanField()),
                ('is_parent', models.NullBooleanField()),
                ('friend', models.ForeignKey(related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='StudentSection',
            new_name='UserSection',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='user',
        ),
        migrations.RemoveField(
            model_name='parentstudent',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='parentstudent',
            name='student',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usersection',
            name='student',
        ),
        migrations.AddField(
            model_name='usersection',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='section',
            name='teacher',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Parent',
        ),
        migrations.DeleteModel(
            name='ParentStudent',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
