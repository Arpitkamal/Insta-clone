# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mydjangoapp', '0005_auto_20170720_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.EmailField(default=0, max_length=254),
        ),
        migrations.AddField(
            model_name='users',
            name='gander',
            field=models.CharField(default='male', max_length=10),
            preserve_default=False,
        ),
    ]
