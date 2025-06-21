from django.shortcuts import get_object_or_404, render, redirect
from books.models import Book
from django.contrib.auth.models import User
from .models import ShopCart, CartItem
from django.contrib import messages, auth


# Create your views here.
def cart(request):
    # Get Shopcart parameter
    shopCart = ShopCart()
    cartItems = CartItem.objects.all()
    context = {"shopCart":shopCart, "cartItems":cartItems}
    return render(request, 'carts/cart.html', context)

def add_to_cart(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        user = User.objects.get(pk=1)  # user is a User instance
        shop_cart, created = ShopCart.objects.get_or_create(userId=user) #assign a User instance to a ForeignKey field (userId),

        unit_price = book.price
        quantity = 1  # or fetch from form data
        sub_total = unit_price * quantity

        # Get or create CartItem
        cart_item, created = CartItem.objects.get_or_create(
            bookId=book,
            shopCartId=shop_cart,
            defaults={
                'quantity': quantity,
                'unit_price': unit_price,
                'sub_total': sub_total
            }
        )
        if not created:
            # If the item exists, update quantity and subtotal
            cart_item.quantity += quantity
            cart_item.sub_total = cart_item.unit_price * cart_item.quantity
            cart_item.save()

        # Fetch all cart items
        cart_items = CartItem.objects.filter(shopCartId=shop_cart)
        total = sum(item.unit_price * item.quantity for item in cart_items)

        return render(request, 'carts/cart.html', {'cart_items': cart_items, 'total': total})
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