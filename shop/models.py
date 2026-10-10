from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

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

