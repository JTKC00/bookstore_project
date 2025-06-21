from django.shortcuts import render, redirect
from .models import ShopCart, CartItem
from django.contrib import messages, auth


# Create your views here.
def cart(request):
    if request.user.is_authenticated:
        try:
            # 嘗試獲取用戶的購物車
            shopcart = request.user.shopcart
            cart_items = shopcart.cart_items.all()
            
            # 檢查購物車是否為空
            if not cart_items.exists():
                messages.info(request, "您的購物車目前是空的，歡迎瀏覽商品並加入購物車。")
            
            return render(request, "carts/cart.html", {
                'shopcart': shopcart,
                'cart_items': cart_items,
                'total_price': shopcart.get_total_price(),
            })
        except AttributeError:
            # 用戶沒有關聯的購物車 - 使用正確的字段名
            shopcart = ShopCart.objects.create(userId=request.user)  
            messages.info(request, "請檢查你的購物清單是否已正確。")
            return render(request, "carts/cart.html", {
                'shopcart': shopcart,
                'cart_items': [],
                'total_price': 0,
            })
    else:
        messages.error(request, "您尚未登入，請先登入以使用購物車功能。")
        return redirect("accounts:login")