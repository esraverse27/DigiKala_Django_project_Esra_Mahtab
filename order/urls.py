from django.urls import path

from .views import *

urlpatterns = [
    path('payment/', payment, name='payment'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
]