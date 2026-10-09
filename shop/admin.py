from django.contrib import admin
from .models import CartItem, CustomerProfile, Order, OrderItem, Product, SellerProfile, Store


class SuperuserOnlyAdmin(admin.ModelAdmin):
    """Allow only superusers to view or manage shop data in Django Admin."""

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(
    (CustomerProfile, SellerProfile, Store, Product, CartItem, Order, OrderItem),
    SuperuserOnlyAdmin,
)
