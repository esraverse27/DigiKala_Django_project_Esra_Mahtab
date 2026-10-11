from django.shortcuts import  redirect, render
from django.core.exceptions import PermissionDenied
from decimal import Decimal, InvalidOperation
from django.db import transaction
from .models import *
from cart.models import CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.permissions import _require_customer

@login_required
def payment(request):
    customer = _require_customer(request)
    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount", ""))
        except (InvalidOperation, TypeError):
            amount = Decimal("0")
        if not amount.is_finite() or amount <= 0 or amount >= Decimal("100000000"):
            messages.error(request, "مبلغ باید بزرگ‌تر از صفر باشد.")
        else:
            customer.balance += amount
            customer.save(update_fields=["balance"])
            messages.success(request, "موجودی آزمایشی افزایش یافت.")
            return redirect("customer_panel")
    return render(request, "payment.html", {"customer": customer})


@login_required
def checkout(request):
    if request.method != "POST":
        raise PermissionDenied
    customer = _require_customer(request)
    with transaction.atomic():
        customer = CustomerProfile.objects.select_for_update().get(pk=customer.pk)
        items = list(CartItem.objects.filter(customer=customer).select_related("product"))
        locked_products = {
            product.pk: product
            for product in Product.objects.select_for_update().filter(
                pk__in=[item.product_id for item in items]
            ).order_by("pk")
        }
        for item in items:
            item.product = locked_products[item.product_id]
            if item.quantity > item.product.stock:
                messages.error(request, f"موجودی {item.product.name} برای تعداد داخل سبد کافی نیست.")
                return redirect("cart")
        total = sum((item.product.price * item.quantity for item in items), Decimal("0"))
        if not items:
            messages.error(request, "سبد خرید خالی است.")
            return redirect("cart")
        if customer.balance < total:
            messages.error(request, "موجودی برای این خرید کافی نیست؛ پرداخت آزمایشی را انجام بده.")
            return redirect("payment")
        order = Order.objects.create(customer=customer, is_paid=True)
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=item.product, quantity=item.quantity)
            for item in items
        ])
        quantities_by_product = {}
        for item in items:
            quantities_by_product[item.product_id] = quantities_by_product.get(item.product_id, 0) + item.quantity
        for product_id, quantity in quantities_by_product.items():
            product = locked_products[product_id]
            product.stock -= quantity
            product.save(update_fields=["stock"])
        customer.balance -= total
        customer.save(update_fields=["balance"])
        CartItem.objects.filter(customer=customer).delete()
    messages.success(request, "سفارش آزمایشی با موفقیت ثبت شد.")
    return redirect("order_history")


@login_required
def order_history(request):
    customer = _require_customer(request)
    orders = list(Order.objects.filter(customer=customer).prefetch_related("orderitem_set__product").order_by("-created_at"))
    for order in orders:
        order.total = sum(
            (line.product.price * line.quantity for line in order.orderitem_set.all()),
            Decimal("0"),
        )
    return render(request, "order_history.html", {"orders": orders})
