from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdminProductForm, AdminStoreForm, ProductForm, SignupForm, StoreForm
from .models import (
    CartItem,
    CustomerProfile,
    Order,
    OrderItem,
    Product,
    SellerProfile,
    Store,
)

STORE_NAME = "مهرا"


def _is_admin(user):
    return user.is_authenticated and user.username == "admin" and user.is_superuser


def _require_admin(request):
    if not _is_admin(request.user):
        raise PermissionDenied


def _require_seller(request):
    if not SellerProfile.objects.filter(user=request.user).exists():
        raise PermissionDenied


def _require_customer(request):
    customer = CustomerProfile.objects.filter(user=request.user).first()
    if customer is None:
        raise PermissionDenied
    return customer


def _seller_store(user):
    return Store.objects.filter(seller__user=user).first()


def _managed_products(user):
    if _is_admin(user):
        return Product.objects.select_related("store").order_by("-id")
    if not SellerProfile.objects.filter(user=user).exists():
        raise PermissionDenied
    store = _seller_store(user)
    if store is None:
        return Product.objects.none()
    return Product.objects.filter(store=store).select_related("store").order_by("-id")


def _seller_products(user):
    """Return only products belonging to the authenticated seller's store."""
    store = _seller_store(user)
    if store is None:
        return Product.objects.none()
    return Product.objects.filter(store=store).select_related("store").order_by("-id")


def home(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.select_related("store").order_by("-id")
    if query:
        products = products.filter(Q(name__icontains=query) | Q(store__name__icontains=query))
    products_by_store = Prefetch("product_set", queryset=products, to_attr="visible_products")
    store_groups = [
        {"store": store, "products": store.visible_products}
        for store in Store.objects.order_by("name").prefetch_related(products_by_store)
        if store.visible_products
    ]
    is_customer = request.user.is_authenticated and CustomerProfile.objects.filter(user=request.user).exists()
    listed_stores = Store.objects.order_by("name")
    if query:
        listed_stores = listed_stores.filter(name__icontains=query)
    return render(request, "home.html", {
        "store_groups": store_groups,
        "stores": listed_stores,
        "query": query,
        "is_customer": is_customer,
    })


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            user = form.save(commit=False)
            user.save()
            if form.cleaned_data["role"] == "seller":
                SellerProfile.objects.create(user=user)
                destination = "seller_panel"
            else:
                CustomerProfile.objects.create(user=user, phone=form.cleaned_data["phone"])
                destination = "customer_panel"
        login(request, user)
        return redirect(destination)
    return render(request, "registration/signup.html", {"form": form})


def _catalog_panel(request, admin_panel):
    if admin_panel:
        _require_admin(request)
        store = None
        store_form = AdminStoreForm()
        product_form = AdminProductForm()
        products = Product.objects.select_related("store").order_by("-id")
        has_store = Store.objects.exists()
        store_name = "همه فروشگاه‌ها"
    else:
        _require_seller(request)
        store = _seller_store(request.user)
        store_form = StoreForm(instance=store)
        product_form = ProductForm()
        products = _seller_products(request.user)
        has_store = store is not None
        store_name = store.name if store else STORE_NAME

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "save_store" and admin_panel:
            store_form = AdminStoreForm(request.POST)
            if store_form.is_valid():
                store_form.save()
                messages.success(request, "فروشگاه ساخته شد.")
                return redirect("manager_panel")
        elif action == "save_store":
            store_form = StoreForm(request.POST, instance=store)
            if store_form.is_valid():
                seller = SellerProfile.objects.get(user=request.user)
                saved_store = store_form.save(commit=False)
                saved_store.seller = seller
                saved_store.save()
                messages.success(request, "اطلاعات فروشگاه ذخیره شد.")
                return redirect("seller_panel")
        elif action == "add_product" and admin_panel:
            product_form = AdminProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, "محصول اضافه شد.")
                return redirect("manager_panel")
        elif action == "add_product":
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                if store is None:
                    product_form.add_error(None, "ابتدا فروشگاه خودت را بساز.")
                else:
                    product = product_form.save(commit=False)
                    product.store = store
                    product.save()
                    messages.success(request, "محصول به فروشگاهت اضافه شد.")
                    return redirect("seller_panel")

    if admin_panel:
        products = Product.objects.select_related("store").order_by("-id")
        stores_to_show = Store.objects.order_by("name")
        has_store = Store.objects.exists()
        store_form = store_form if request.method == "POST" and request.POST.get("action") == "save_store" else AdminStoreForm()
        product_form = product_form if request.method == "POST" and request.POST.get("action") == "add_product" else AdminProductForm()
    else:
        store = _seller_store(request.user)
        products = _seller_products(request.user)
        stores_to_show = [store] if store else []
        has_store = store is not None
        store_form = store_form if request.method == "POST" and request.POST.get("action") == "save_store" else StoreForm(instance=store)
        product_form = product_form if request.method == "POST" and request.POST.get("action") == "add_product" else ProductForm()
        store_name = store.name if store else STORE_NAME

    product_prefetch = Prefetch("product_set", queryset=Product.objects.order_by("-id"), to_attr="panel_products")
    if admin_panel:
        stores_to_show = Store.objects.order_by("name").prefetch_related(product_prefetch)
    elif store:
        stores_to_show = [Store.objects.filter(pk=store.pk).prefetch_related(
            Prefetch("product_set", queryset=_seller_products(request.user), to_attr="panel_products")
        ).first()]
    store_groups = [
        {"store": listed_store, "products": listed_store.panel_products}
        for listed_store in stores_to_show
    ]

    return render(request, "manager_panel.html", {
        "store_form": store_form,
        "store": store,
        "has_store": has_store,
        "product_form": product_form,
        "store_name": store_name,
        "store_groups": store_groups,
        "product_count": products.count(),
        "is_admin_panel": admin_panel,
        "panel_url": "manager_panel" if admin_panel else "seller_panel",
    })


@login_required
def manager_panel(request):
    return _catalog_panel(request, admin_panel=True)


@login_required
def seller_panel(request):
    return _catalog_panel(request, admin_panel=False)


@login_required
def manager_edit_product(request, product_id):
    products = _managed_products(request.user)
    product = get_object_or_404(products, pk=product_id)
    admin_mode = _is_admin(request.user)
    form_class = AdminProductForm if admin_mode else ProductForm
    old_image_name = product.image.name
    old_image_storage = product.image.storage
    form = form_class(request.POST or None, request.FILES or None, instance=product)
    form.fields["image"].required = False
    if request.method == "POST" and form.is_valid():
        updated_product = form.save()
        if old_image_name and updated_product.image.name != old_image_name:
            old_image_storage.delete(old_image_name)
        messages.success(request, "تغییرات محصول ذخیره شد.")
        return redirect("manager_panel" if admin_mode else "seller_panel")
    return render(request, "manager_product_edit.html", {
        "form": form,
        "product": product,
        "store_name": product.store.name,
        "panel_url": "manager_panel" if admin_mode else "seller_panel",
    })


@login_required
def manager_delete_product(request, product_id):
    products = _managed_products(request.user)
    product = get_object_or_404(products, pk=product_id)
    admin_mode = _is_admin(request.user)
    if request.method == "POST":
        if product.image:
            product.image.delete(save=False)
        product.delete()
        messages.success(request, "محصول و تصویرش حذف شد.")
        return redirect("manager_panel" if admin_mode else "seller_panel")
    return render(request, "manager_product_delete.html", {
        "product": product,
        "store_name": product.store.name,
        "panel_url": "manager_panel" if admin_mode else "seller_panel",
    })


@login_required
def customer_panel(request):
    customer = _require_customer(request)
    return render(request, "customer_panel.html", {"customer": customer})


def stores(request):
    return render(request, "stores.html", {"stores": Store.objects.order_by("name")})


def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    products = Product.objects.filter(store=store).order_by("-id")
    is_owner = request.user.is_authenticated and store.seller.user_id == request.user.id
    is_customer = request.user.is_authenticated and CustomerProfile.objects.filter(user=request.user).exists()
    return render(request, "store_detail.html", {
        "store": store,
        "products": products,
        "is_owner": is_owner,
        "is_customer": is_customer,
    })


@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        raise PermissionDenied
    customer = _require_customer(request)
    product = get_object_or_404(Product, pk=product_id)
    item = CartItem.objects.filter(customer=customer, product=product).first()
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
