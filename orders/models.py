from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from datetime import datetime
from carts.models import ShopCart, CartItem


class Order(models.Model):
    userId = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    shopCartId = models.ForeignKey(ShopCart, on_delete=models.DO_NOTHING)
    invoice_no = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now_add=True)
    receipient = models.CharField(max_length=50)
    receipient_phone = models.CharField(max_length=20)
    shipping_address = models.CharField(max_length=200)
    payment_status = models.CharField(max_length=5)
    shipping_status = models.CharField(max_length=5)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    bookid = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    CartID = models.ForeignKey(CartItem, on_delete=models.DO_NOTHING)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    subTotal = models.DecimalField(max_digits=10, decimal_places=2)
