from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manager/', views.manager_panel, name='manager_panel'),
    path('seller/', views.seller_panel, name='seller_panel'),
    path('customer/', views.customer_panel, name='customer_panel'),
    path('stores/', views.stores, name='stores'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/', views.payment, name='payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('manager/products/<int:product_id>/edit/', views.manager_edit_product, name='manager_edit_product'),
    path('manager/products/<int:product_id>/delete/', views.manager_delete_product, name='manager_delete_product'),
    path('seller/products/<int:product_id>/edit/', views.manager_edit_product, name='seller_edit_product'),
    path('seller/products/<int:product_id>/delete/', views.manager_delete_product, name='seller_delete_product'),
]
