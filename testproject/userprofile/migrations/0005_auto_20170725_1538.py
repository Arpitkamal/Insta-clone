# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 10:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20170724_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='fullname',
            new_name='name',
        ),
    ]
