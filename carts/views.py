from django.shortcuts import render
# from .models import ShopCart, CartItem


# Create your views here.
def carts(request):
    return render(request, "carts/cart.html")
