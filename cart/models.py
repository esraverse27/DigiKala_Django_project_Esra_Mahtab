from django.db import models
from shop.models import *

class CartItem(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class cart(models.Model):
    user = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
