from django.shortcuts import render
# from .models import ShopCart, CartItem


# Create your views here.
def cart(request):
    return render(request, "carts/cart.html")
