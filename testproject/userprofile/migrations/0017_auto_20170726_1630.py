# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 11:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0016_auto_20170726_1313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='name',
            new_name='fullname',
        ),
    ]