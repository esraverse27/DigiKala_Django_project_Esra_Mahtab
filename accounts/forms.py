from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignupForm(UserCreationForm):
    role = forms.ChoiceField(
        label="نوع حساب",
        choices=(("customer", "مشتری"), ("seller", "فروشنده")),
    )
    phone = forms.CharField(label="شماره تماس", max_length=11, required=True)
    first_name = forms.CharField(label="نام", max_length=100, required=False)
    last_name = forms.CharField(label="نام خانوادگی", max_length=100, required=False)

class UserLoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "نام کاربری یا رمز عبور نادرست است.",
        "inactive": "این حساب غیرفعال است.",
    }
    username = forms.CharField(
        label="شماره تلفن",
        max_length=11,
        widget=forms.TextInput(attrs={"autocomplete": "tel", "autofocus": True}),
    )
    password = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
