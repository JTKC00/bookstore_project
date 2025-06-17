from django.db import models
from datetime import datetime

# Create your models here.
class ShopCart(models.Model):
    datetime = models.DateTimeField(default=datetime.now, blank=True)
    user_id = models.IntegerField(blank=True)
    

class CartItem(models.Model):
    bookId = models.CharField(max_length=100)
    shopCartId = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    sub_total = models.DecimalField(max_digits=2, decimal_places=1)
    unit_price = models.DecimalField(max_digits=2, decimal_places=1)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)