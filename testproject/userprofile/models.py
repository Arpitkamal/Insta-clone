# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
"""
this class is for user profile
"""
class usermodel(models.Model):
    email=models.EmailField(unique=True,null=False,blank=False)
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=200,unique=True,null=False,blank=False)
    password=models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class UserSessionToken(models.Model):
    user=models.ForeignKey(usermodel,on_delete=models.PROTECT) #on_delete will protect from deletion
    session_token=models.CharField(max_length=250)
    created_on=models.DateTimeField(auto_now_add=True)
    is_valid=models.BooleanField(default=True)

    def create_token(self):
        from uuid import uuid4

        self.session_token=uuid4()