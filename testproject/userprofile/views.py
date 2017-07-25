# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render,redirect
from forms import SignUpForm,LoginForm
from django.template import loader
from models import usermodel,UserSessionToken
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password ,check_password


# Create your views here.
def signup_view(request):
    import datetime

    if request.method =="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user=usermodel(fullname=name,password=make_password(password),Email=email,username=username)
            user.save()
            return render(request,'success.html')


    else:
        signup_form = SignUpForm()
        template=loader.get_template('userprofile/index.html')
        return render(request , 'userprofile/index.html',{'form': signup_form})



def login_view(request):
    import datetime

    if request.method =="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            user=usermodel.objects.filter(username=form.cleaned_data['username']).first()
            if user:
                check_password(form.cleaned_data['password'],user.password)
                SESS=UserSessionToken(user=user)
                SESS.creat_token()
                SESS.save()
                response=redirect('feed/')
                response.set_cookie(key='session_token', value=token.session_token)
                return response
            else:
                print "user is Invalid"
            render(request,'success.html')
    elif request.method== "GET":
        template=loader.get_template('userprofile/index.html')
        login_form=LoginForm()
        date=datetime.datetime.now()
    return render(request , 'userprofile/index.html',{'hun_da_time':date})
