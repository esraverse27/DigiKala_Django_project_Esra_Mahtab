from django.db import models
from shop.models import *

class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
