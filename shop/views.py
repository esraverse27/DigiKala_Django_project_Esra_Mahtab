from django.shortcuts import render

from .models import Product

def home(request):
    products = Product.objects.select_related('store').order_by('-id')
    return render(request, 'home.html', {'products': products})
