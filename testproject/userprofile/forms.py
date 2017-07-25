from django import forms
from userprofile.models import usermodel

class SignUpForm(forms.ModelForm):

    class Meta:
        model=usermodel
        fields= ['Email','username','fullname','password']


class LoginForm(forms.ModelForm):

    class Meta:
        model=usermodel
        fields=['username','password']