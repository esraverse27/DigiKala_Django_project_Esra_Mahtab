from django.db import models

# Create your models here.

from django.contrib.auth.models import User

# Profiles
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Seller-specific fields can be added here

# Core Entities
class Store(models.Model):
    seller = models.OneToOneField(SellerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

class Product(models.Model):
    class Category(models.TextChoices):
        CLOTHING = "clothing", "پوشاک"
        HYGIENE = "hygiene", "بهداشتی"
        JEWELRY = "jewelry", "طلا و جواهرات"
        COSMETICS = "cosmetics", "لوازم آرایشی"

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.CLOTHING,
        verbose_name="دسته‌بندی",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")

# Transactions
class CartItem(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
