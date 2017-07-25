# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mydjangoapp', '0003_users_modified_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='name',
        ),
        migrations.AddField(
            model_name='users',
            name='text',
            field=models.CharField(default='arpit', max_length=250),
            preserve_default=False,
        ),
    ]
