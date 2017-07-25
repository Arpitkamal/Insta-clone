# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models

class user(models.Model):
    name=models.CharField(max_length=250, null=False , blank=False)
    phone=models.CharField(max_length=30)
    age=models.IntegerField(default=0)
    gander=models.CharField(max_length=10, null=False)
    email=models.EmailField(default=0,null=False)
    has_verified_mobile=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now=True)
    modified_date=models.DateTimeField(auto_now_add=True)

