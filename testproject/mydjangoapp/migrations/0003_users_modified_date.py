# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 19:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mydjangoapp', '0002_auto_20170719_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='modified_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
