# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trailHQ', '0002_singletrackstrail_latitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='singletrackstrail',
            name='id',
        ),
        migrations.AddField(
            model_name='singletrackstrail',
            name='key',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
