from django.db import models
from datetime import datetime

# Create your models here.
# class ShopCart(models.Model):
#     created_at = models.DateTimeField(default=datetime.now)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    

# class CartItem(models.Model):
#     bookId = models.CharField(max_length=100)
#     shopCartId = models.ForeignKey(ShopCart, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     sub_total = models.DecimalField(max_digits=2, decimal_places=1)
#     unit_price = models.DecimalField(max_digits=2, decimal_places=1)