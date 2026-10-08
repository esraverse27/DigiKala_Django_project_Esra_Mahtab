from django.contrib import admin
from .models import CartItem, CustomerProfile, Order, OrderItem, Product, SellerProfile, Store

admin.site.register((CustomerProfile, SellerProfile, Store, Product, CartItem, Order, OrderItem))
