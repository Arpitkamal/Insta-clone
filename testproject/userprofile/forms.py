from django import forms
from models import usermodel,Postmodal,Commentmodel,Likemodel,CommentLikeModel

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
        model=Commentmodel
        fields=['comment_text','post']


class CommentLikeForm(forms.ModelForm):

    class Meta:
        model=CommentLikeModel
        fields=['comment']

