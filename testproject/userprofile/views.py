# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render,redirect
from forms import SignUpForm,LoginForm,PostForm,LikeForm,CommentForm
from django.template import loader
from models import usermodel,UserSessionToken,Postmodal,Likemodel,Commentmodel
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password ,check_password
from imgurpython import ImgurClient
from testproject.settings import BASE_DIR
from datetime import timedelta
from django.utils import timezone
import os
from clarifai.rest import ClarifaiApp
import ctypes
USER_CLIENT_ID='eadc92c53ed9e6e'
USER_CLIENT_SECRET='f392bcdca7698d2928f9157d230cefc62d62e554'


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
    if request.method =="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=usermodel.objects.filter(username=username).first()
            if user:
               if check_password(password,user.password):
                    SESS=UserSessionToken(user=user)
                    SESS.Create_token()
                    SESS.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=SESS.session_token)
                    return response
               else:
                   print "password is incorrect "
            else:
                print "user is Invalid"
    elif request.method=="GET":
        login_form=LoginForm()
    return render(request , 'login.html',{'from':login_form})



def feed_view(request):
    user=check_validation(request)
    if user:
        posts=Postmodal.objects.all().order_by('created_on')

        for post in posts:
            existing_like=Likemodel.objects.filter(post_id=post.id,user=user).first()
            if existing_like:
                post.has_like=True

        return render(request, 'feed.html',{'posts': posts})
    else:
        return render('/login/')



def Post_view(request):
    user=check_validation(request)
    if user:
        if request.method=="POST":
            form=PostForm(request.POST,request.FILES)
            if form.is_valid():
                image=form.cleaned_data.get('image')
                caption=form.cleaned_data.get('caption')
                user=Postmodal(user=user,image=image,caption=caption)
                user.save()
                path=os.path.join(BASE_DIR,user.image.url)
                client=ImgurClient(USER_CLIENT_ID,USER_CLIENT_SECRET)
                user.image_url=client.upload_from_path(path,anon=True)['link']
                app = ClarifaiApp(api_key="aa14b38a0332430789ff7aebdcdd466b")
                model = app.models.get("nsfw-v1.0")
                response=model.predict_by_url(url=user.image_url)
                i=len(response["outputs"])
                i-=1
                if response["outputs"][i]["data"]["concepts"][1]>response["outputs"][i]["data"]["concepts"][0]:
                    ctypes.windll.user32.MessageBoxW(0, u"Warning!! you are uploading adult content", u"Error", 0)
                else:
                    user.save()
                return redirect('/feed/')
        elif request.method=="GET":
            form=PostForm()
        return render(request,'post.html',{'form':form})
    else:
        redirect('/login/')


def feed_view(request):
    user=check_validation(request)
    if user:
        posts=Postmodal.objects.all().order_by('-created_on')

        for post in posts:
            existing_like=Likemodel.objects.filter(post_id=post.id,user=user).first()
            if existing_like:
                post.has_like=True

        return render(request,"feed.html",{"posts":posts})
    else:
        return render('/login/')


def like_view(request):
    user=check_validation(request)
    if user and request.method=="POST":
        form=LikeForm(request.POST)
        if form.is_valid():
            post_id=form.cleaned_data.get("post").id
            existing_like=Likemodel.objects.filter(post_id=post_id,user=user).first()
            if not existing_like:
                Likemodel.objects.create(post_id=post_id,user=user)
                ctypes.windll.user32.MessageBoxW(0, u"liked successfully", u"SUCCESS", 0)
            else:
                 existing_like.delete()
                 ctypes.windll.user32.MessageBoxW(0, u"unlike successfully", u"SUCCESS", 0)

            return redirect("/feed/")

    else:
        return redirect("/login/")



def comment_view(request):
    user=check_validation(request)
    if user and request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            post_id=form.cleaned_data.get("post").id
            comment_text=form.cleaned_data.get("comment_text")
            comment=Commentmodel.objects.create(user=user,post_id=post_id,comment_text=comment_text)
            comment.save()
            ctypes.windll.user32.MessageBoxW(0, u"comment posted successfully", u"SUCCESS", 0)
            return redirect("feed/")
        else:
            return redirect("feed/")
    else:
        return redirect('login/')

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = UserSessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
            else:
                return None


def logout_view(request):
    if request.COOKIES.get("session_token"):
        session=UserSessionToken.objects.filter(session_token=request.COOKIES.get("session_token")).first()
        if session:
            session.delete()
            return render(request,"logout.html")
    else:
        return None