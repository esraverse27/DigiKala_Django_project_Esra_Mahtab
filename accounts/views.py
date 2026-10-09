from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            form = UserLoginForm()
            return render(request, 'registration/login.html', {'error':'نام کاربری یا رمز عبور اشتباه است', 'form':form})

    else:
        form = UserLoginForm()
        return render(request, 'registration/login.html', {'form':form})


def signin_view(request):
    from shop.views import signup
    return signup(request)

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

def home_view(request):
    return render(request, 'home.html')
