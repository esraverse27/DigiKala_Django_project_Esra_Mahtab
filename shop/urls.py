from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('manager/', manager_panel, name='manager_panel'),
    path('seller/', seller_panel, name='seller_panel'),
    path('customer/', customer_panel, name='customer_panel'),
    path('stores/', stores, name='stores'),
    path('stores/<int:store_id>/', store_detail, name='store_detail'),
    path('cart/', cart, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('payment/', payment, name='payment'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path('manager/products/<int:product_id>/edit/', manager_edit_product, name='manager_edit_product'),
    path('manager/products/<int:product_id>/delete/', manager_delete_product, name='manager_delete_product'),
    path('seller/products/<int:product_id>/edit/', manager_edit_product, name='seller_edit_product'),
    path('seller/products/<int:product_id>/delete/', manager_delete_product, name='seller_delete_product'),
]
