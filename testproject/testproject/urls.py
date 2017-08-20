"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from userprofile.views import signup_view,login_view,feed_view,Post_view,like_view,comment_view,logout_view,upvote_comment_view,particular_user_post

urlpatterns = [
    url(r'^login/feed/(?P<user_name>[a-zA-Z]+)/$',particular_user_post),
    url('upvote/',upvote_comment_view),
    url('logout/',logout_view),
    url('comment/',comment_view),
    url('like/',like_view),
    url('post/', Post_view),
    url('feed/', feed_view),
    url('login/',login_view),
    url('^',signup_view),

]
