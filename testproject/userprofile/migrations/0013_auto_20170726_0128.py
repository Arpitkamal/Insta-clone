# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 19:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0012_auto_20170726_0118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='name',
            new_name='fullname',
        ),
    ]
