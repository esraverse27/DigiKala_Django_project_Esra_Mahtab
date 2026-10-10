from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.exceptions import PermissionDenied
from .forms import *
from shop.models import SellerProfile, CustomerProfile
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "registration/login.html", {"form": form})


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    form = SignupForm(request.POST)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.save()
        #
        if form.cleaned_data["role"] == "seller":
            SellerProfile.objects.create(user=user)
            destination = "seller_panel"
        else:
            CustomerProfile.objects.create(user=user, phone=form.cleaned_data["phone"])
        login(request, user)
        return redirect('customer_panel')
    return render(request, "registration/signup.html", {"form": form})


@login_required
def logout_view(request):
    if request.method != "POST":
        raise PermissionDenied
    logout(request)
    return render(request, "registration/logged_out.html")





