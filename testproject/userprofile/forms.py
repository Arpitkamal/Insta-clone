from django import forms
from userprofile.models import usermodel,Postmodal,Commentmodel,Likemodel

class SignUpForm(forms.ModelForm):

    class Meta:
        model=usermodel
        fields= ['email','username','name','password']


class LoginForm(forms.ModelForm):

    class Meta:
        model=usermodel
        fields=['username','password']

class PostForm(forms.ModelForm):

    class Meta:
        model=Postmodal
        fields=['image','caption']


class LikeForm(forms.ModelForm):

     class Meta:
         model=Likemodel
         fields=['post']

class CommentForm(forms.ModelForm):

    class Meta:
        modul=Commentmodel
        fields=['comment_text','post']