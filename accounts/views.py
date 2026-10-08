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
            return render(request, 'registration/login.html', {'error':'username or password is incorrect', 'form':form})

    else:
        form = UserLoginForm()
        return render(request, 'registration/login.html', {'form':form})


def signin_view(request):
    if not request.user.is_authenticated:
    
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return render(request, 'home.html')
            return render(request, 'registration/signup.html', {'form':form})

        else:
            form = UserRegisterForm()
            return render(request, 'registration/signup.html', {'form':form})

    else:
        return redirect('home')

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

def home_view(request):
    return render(request, 'home.html')
