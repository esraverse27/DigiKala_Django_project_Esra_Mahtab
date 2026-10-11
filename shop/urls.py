from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('manager/', manager_panel, name='manager_panel'),
    path('seller/', seller_panel, name='seller_panel'),
    path('customer/', customer_panel, name='customer_panel'),
    path('stores/', stores, name='stores'),
    path('stores/<int:store_id>/', store_detail, name='store_detail'),
    path('manager/products/<int:product_id>/edit/', manager_edit_product, name='manager_edit_product'),
    path('manager/products/<int:product_id>/delete/', manager_delete_product, name='manager_delete_product'),
    path('seller/products/<int:product_id>/edit/', manager_edit_product, name='seller_edit_product'),
    path('seller/products/<int:product_id>/delete/', manager_delete_product, name='seller_delete_product'),
]
