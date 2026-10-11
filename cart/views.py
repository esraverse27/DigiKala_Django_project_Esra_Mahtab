from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from decimal import Decimal
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.permissions import _require_customer


@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        raise PermissionDenied
    customer = _require_customer(request)
    product = get_object_or_404(Product, pk=product_id)
    item = CartItem.objects.filter(customer=customer, product=product).first()
    current_quantity = item.quantity if item else 0
    if product.stock < 1:
        messages.error(request, "این محصول در حال حاضر ناموجود است.")
        return redirect("cart")
    if current_quantity >= product.stock:
        messages.error(request, "تعداد درخواستی از موجودی فروشگاه بیشتر است.")
        return redirect("cart")
    if item:
        item.quantity += 1
        item.save(update_fields=["quantity"])
    else:
        CartItem.objects.create(customer=customer, product=product)
    messages.success(request, "محصول به سبد خرید اضافه شد.")
    return redirect("cart")


@login_required
def cart(request):
    customer = _require_customer(request)
    items = list(CartItem.objects.filter(customer=customer).select_related("product", "product__store"))
    for item in items:
        item.line_total = item.product.price * item.quantity
    total = sum((item.line_total for item in items), Decimal("0"))
    return render(request, "cart.html", {"cart_items": items, "total": total})


@login_required
def update_cart_item(request, item_id):
    if request.method != "POST":
        raise PermissionDenied
    customer = _require_customer(request)
    item = get_object_or_404(CartItem, pk=item_id, customer=customer)
    try:
        quantity = int(request.POST.get("quantity", ""))
    except (TypeError, ValueError):
        quantity = 0
    if quantity < 1 or quantity > 999:
        messages.error(request, "تعداد باید بین ۱ تا ۹۹۹ باشد.")
    elif quantity > item.product.stock:
        messages.error(request, f"از این محصول فقط {item.product.stock} عدد موجود است.")
    else:
        item.quantity = quantity
        item.save(update_fields=["quantity"])
        messages.success(request, "تعداد محصول در سبد خرید به‌روزرسانی شد.")
    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    if request.method != "POST":
        raise PermissionDenied
    customer = _require_customer(request)
    item = get_object_or_404(CartItem, pk=item_id, customer=customer)
    item.delete()
    messages.success(request, "محصول از سبد حذف شد.")
    return redirect("cart")

