from django import forms
from . import models
class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'password']
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
class Request(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    firstsetting = forms.CharField(max_length=255)
    secondsetting = forms.CharField(max_length=255)