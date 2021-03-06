# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20170724_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(max_length=250)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userprofile.usermodel')),
            ],
        ),
    ]
