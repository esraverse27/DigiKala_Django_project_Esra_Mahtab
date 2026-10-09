from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserRegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=11, label='phone')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=11, label='شماره تلفن')
    password = forms.CharField(widget=forms.PasswordInput)
