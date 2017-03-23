# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trailHQ', '0003_auto_20170315_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrackstrail',
            name='difficulty',
            field=models.TextField(default=2.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='singletrackstrail',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=2.0, max_digits=3),
        ),
    ]
