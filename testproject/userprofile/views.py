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
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=usermodel(name=name,username=username,email=email,password=make_password(password))
            user.save()
            return render(request,'success.html')
    elif request.method=="GET":
        signup_form=SignUpForm()
        date=datetime.datetime.now()
    return render(request , 'index.html',{'form': signup_form,'hun_da_time':date},)



def login_view(request):
    import datetime

    if request.method =="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=usermodel.objects.filter(username=username).first()
            if user:
                check_password(password,user.password)
                SESS=UserSessionToken(user=user)
                SESS.creat_token()
                SESS.save()
                response=redirect('feed/')
                response.set_cookie(key='session_token', value=SESS.session_token)
                return response
            else:
                print "user is Invalid"
            render(request,'success.html')
    elif request.method== "GET":
        login_form=LoginForm()
        date=datetime.datetime.now()
    return render(request , 'login.html',{'hun_da_time':date})



def feed_view(request):
    return render(request, 'feed.html')

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session=UserSessionToken.object.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
        else:
            return None