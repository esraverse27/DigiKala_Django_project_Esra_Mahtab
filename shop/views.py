from django.db.models import Q
from django.shortcuts import render

from .models import Product


def home(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.select_related('store').order_by('-id')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(store__name__icontains=query)
        )

    return render(request, 'home.html', {
        'products': products,
        'query': query,
    })
