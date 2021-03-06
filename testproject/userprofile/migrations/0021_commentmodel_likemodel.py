# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0020_auto_20170730_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentmodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=1000)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.Postmodal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='Likemodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.Postmodal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.usermodel')),
            ],
        ),
    ]
