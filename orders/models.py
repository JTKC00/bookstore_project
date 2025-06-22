from django.db import models
from datetime import datetime
from carts.models import ShopCart
from books.models import Book
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    shopCartId = models.ForeignKey(ShopCart, on_delete=models.DO_NOTHING)
    invoice_no = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipient = models.CharField(max_length=100)
    receipient_phone = models.CharField(max_length=15)
    shipping_address = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=50)
    shipping_status = models.CharField(max_length=50)

class OrderItem(models.Model):
    bookid = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    orderid = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
