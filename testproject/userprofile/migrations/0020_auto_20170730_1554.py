# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0019_postmodal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(max_length=200),
        ),
    ]
