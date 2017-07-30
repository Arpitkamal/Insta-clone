from django import forms
from userprofile.models import usermodel,Postmodal

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