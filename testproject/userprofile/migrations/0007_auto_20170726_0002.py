# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 18:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_auto_20170725_2344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='email',
            new_name='Email',
        ),
    ]
