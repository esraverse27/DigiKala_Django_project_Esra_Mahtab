from django.db import models
from accounts.models import User


class Store(models.Model):
    Name = models.CharField(max_lenght=100, unique=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_lenght=11, blank=True)
    address = models.TextField(blank=True)

class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_lenght=100)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_lenght=100, unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
