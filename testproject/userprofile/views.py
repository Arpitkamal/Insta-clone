# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from forms import SignUpForm,LoginForm,PostForm,LikeForm,CommentForm,CommentLikeForm
from django.template import loader
from models import usermodel,UserSessionToken,Postmodal,Likemodel,Commentmodel,CommentLikeModel
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password ,check_password
from imgurpython import ImgurClient
from testproject.settings import BASE_DIR
from datetime import timedelta
from django.utils import timezone
import os
from clarifai.rest import ClarifaiApp
import ctypes
import sendgrid
from sendgrid.helpers.mail import *
import requests,json
USER_CLIENT_ID=''
USER_CLIENT_SECRET=''
SENDGRID_API_KEY=""
PARALLELDOTS_KEY=""


# view for signup.html
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
            sg = sendgrid.SendGridAPIClient(apikey=(SENDGRID_API_KEY)) # using sandgrid api to send mails
            from_email = Email("kamalarpit@yahoo.in")
            to_email = Email(email)
            subject = "Successfully login "
            content = Content("text/plain", "thank you for sign up")
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
            ctypes.windll.user32.MessageBoxW(0, u"successfully signed up", u"success", 0)
            return render(request,'success.html')

    elif request.method=="GET":
        signup_form=SignUpForm()
        date=datetime.datetime.now()
    return render(request , 'index.html',{'form': signup_form,'hun_da_time':date})


# view for login.html
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
                   ctypes.windll.user32.MessageBoxW(0, u"invalid username or password", u"Error", 0)
            else:
                ctypes.windll.user32.MessageBoxW(0, u"invalid username", u"Error", 0)
    elif request.method=="GET":
        login_form=LoginForm()
    return render(request , 'login.html',{'from':login_form})


# view for feed.html
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


# view for post.html
def Post_view(request):
    user=check_validation(request)
    if user:
        if request.method=="POST":
            form=PostForm(request.POST,request.FILES)
            if form.is_valid():
                image=form.cleaned_data.get('image')
                caption=form.cleaned_data.get('caption')
                url = "http://apis.paralleldots.com/abuse"  #using paralleldots api to detect Abusive content in caption
                r = requests.post(url, params={"apikey": PARALLELDOTS_KEY, "text": caption})
                caption_text = r.text
                data = json.loads(caption_text)
                if data['sentence_type'] == 'Abusive':
                    print data['confidence_score']
                    ctypes.windll.user32.MessageBoxW(0, u"Your caption contain Abusive content", u"Warning", 0)
                    return redirect('/post/')
                else:
                    user=Postmodal(user=user,image=image,caption=caption)
                    user.save()
                    path=os.path.join(BASE_DIR,user.image.url)
                    client=ImgurClient(USER_CLIENT_ID,USER_CLIENT_SECRET)
                    user.image_url=client.upload_from_path(path,anon=True)['link']
                    user.save()
                    app = ClarifaiApp(api_key='aa14b38a0332430789ff7aebdcdd466b')
                    model = app.models.get('nsfw-v1.0')
                    response=model.predict_by_url(url=user.image_url)
                    image_response=response['outputs'][0]['data']['concepts']
                    for i in image_response:
                        if i['name']=='nsfw':
                            image_value=i['value']
                            if image_value>=0.85:
                                print response['outputs'][0]['data']['concepts']
                                print image_value
                                user.delete()
                                error_message="you are trying to post inappropriate image"
                                return render(request,'error.html',{'error_message':error_message})
                        else:
                            return redirect('/feed/')
        elif request.method=="GET":
            form=PostForm()
        return render(request,'post.html',{'form':form})
    else:
        redirect('/login/')


#view for like on post
def like_view(request):
    user=check_validation(request)
    if user and request.method=="POST":
        form=LikeForm(request.POST)
        if form.is_valid():
            post_id=form.cleaned_data.get("post").id
            existing_like=Likemodel.objects.filter(post_id=post_id,user=user).first()
            if not existing_like:
                like=Likemodel.objects.create(post_id=post_id,user=user)
                sg = sendgrid.SendGridAPIClient(apikey=(SENDGRID_API_KEY))
                from_email = Email("kamalarpit@yahoo.in")
                to_email = Email(like.post.user.email)
                subject = "like on your post"
                content = Content("text/plain", "someone just like your post")
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                print(response.status_code)
                print(response.body)
                print(response.headers)
                ctypes.windll.user32.MessageBoxW(0, u"liked successfully", u"SUCCESS", 0)
            else:
                 existing_like.delete()
                 ctypes.windll.user32.MessageBoxW(0, u"unlike successfully", u"SUCCESS", 0)

            return redirect("/feed/")

    else:
        return redirect("/login/")


# view for comment on post
def comment_view(request):
    user=check_validation(request)
    if user and request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            post_id=form.cleaned_data.get('post').id
            comment_text=form.cleaned_data.get("comment_text")
            url = "http://apis.paralleldots.com/abuse" #using paralleldots api to detect Abusive content in comment
            r = requests.post(url, params={"apikey": PARALLELDOTS_KEY, "text": comment_text})
            caption_text = r.text
            data = json.loads(caption_text)
            if data['sentence_type'] == 'Abusive':
                print data['confidence_score']
                ctypes.windll.user32.MessageBoxW(0, u"You are commenting Abusive content", u"Warning", 0)
                return redirect('/feed/')
            else:
                comment=Commentmodel.objects.create(user=user,post_id=post_id,comment_text=comment_text)
                comment.save()
                sg = sendgrid.SendGridAPIClient(apikey=(SENDGRID_API_KEY))
                from_email = Email("kamalarpit@yahoo.in")
                to_email = Email(comment.user.email)
                subject = "comment on your post"
                content = Content("text/plain", "someone just comment on your post")
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                print(response.status_code)
                print(response.body)
                print(response.headers)
                ctypes.windll.user32.MessageBoxW(0, u"comment posted successfully", u"SUCCESS", 0)
                return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login/')

#view for upvote on comment
def upvote_comment_view(request):
    user=check_validation(request)
    if user and request.method=="POST":
        form=CommentLikeForm(request.POST)
        if form.is_valid():
            comment_id=form.cleaned_data.get('comment').id
            existed_like=CommentLikeModel.objects.filter(comment_id=comment_id,user=user).first()
            if not existed_like:
                CommentLikeModel.objects.create(comment_id=comment_id,user=user)
                Commentmodel.has_upvoted=True
                ctypes.windll.user32.MessageBoxW(0, u"comment is upvoted successfully", u"SUCCESS", 0)
            else:
                existed_like.delete()
                Commentmodel.has_upvoted=False
                ctypes.windll.user32.MessageBoxW(0, u"comment downvoted successfully", u"SUCCESS", 0)

        return redirect('/feed/')
    else:
        return redirect('/login/')

def particular_user_post(request,user_name):
    user=check_validation(request)
    if user:
        post=Postmodal.objects.all().filter(username=user_name).first()
        return render(request,'postofuser.html',{'posts':post,'username':user_name})
    else:
        return redirect('/login/')


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = UserSessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
            else:
                return None

#view for logout.html
def logout_view(request):
    if request.COOKIES.get("session_token"):
        session=UserSessionToken.objects.filter(session_token=request.COOKIES.get("session_token")).first()
        if session:
            session.delete()
            return render(request,"logout.html")
    else:
        return None

