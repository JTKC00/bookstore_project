from django.shortcuts import get_object_or_404, render, redirect
from books.models import Book
from .models import ShopCart, CartItem
from django.contrib import messages
from django.http import JsonResponse

def cart(request):
    if request.user.is_authenticated:
        try:
            # 獲取用戶的購物車
            shopcart = ShopCart.objects.get(userId=request.user)
            
            # 使用默認的反向關聯名
            cart_items = shopcart.cartitem_set.all()
            
            # 計算總數量和總價格
            total_quantity = sum(item.quantity for item in cart_items)
            total_price = sum(item.sub_total for item in cart_items)
            
            # 檢查購物車是否為空
            if not cart_items.exists():
                messages.info(request, "您的購物車目前是空的，歡迎瀏覽商品並加入購物車。")
            
            return render(request, "carts/cart.html", {
                'shopcart': shopcart,
                'cart_items': cart_items,
                'total_quantity': total_quantity,
                'total_price': total_price,
            })
        except ShopCart.DoesNotExist:
            # 用戶沒有購物車，創建一個新的
            shopcart = ShopCart.objects.create(userId=request.user)
            messages.info(request, "已為您創建新的購物車，現在可以開始購物了。")
            return render(request, "carts/cart.html", {
                'shopcart': shopcart,
                'cart_items': [],
                'total_quantity': 0,
                'total_price': 0,
            })
    else:
        messages.error(request, "您尚未登入，請先登入以使用購物車功能。")
        return redirect("accounts:login")

def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        messages.error(request, "您尚未登入，請先登入以使用購物車功能。")
        return redirect("accounts:login")
        
    book = get_object_or_404(Book, pk=book_id)
    
    # 獲取或創建用戶購物車
    shop_cart, created = ShopCart.objects.get_or_create(userId=request.user)

    unit_price = book.price
    quantity = 1  # 或從表單獲取數量
    sub_total = unit_price * quantity

    # 獲取或創建購物車項目
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
        # 如果項目已存在，更新數量和小計
        cart_item.quantity += quantity
        cart_item.sub_total = cart_item.unit_price * cart_item.quantity
        cart_item.save()
        messages.success(request, f"已將 {book.title} 的數量增加至 {cart_item.quantity}。")
    else:
        messages.success(request, f"{book.title} 已成功添加到購物車。")

    # 重定向到購物車頁面
    return redirect('carts:cart')

def update_quantity(request, item_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "請先登入"}, status=401)
        
    cart_item = get_object_or_404(CartItem, pk=item_id)
    
    # 確保用戶只能修改自己的購物車
    if cart_item.shopCartId.userId != request.user:
        return JsonResponse({"error": "無權限修改此項目"}, status=403)
    
    action = request.GET.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
    
    cart_item.sub_total = cart_item.unit_price * cart_item.quantity
    cart_item.save()
    
    # 重新計算購物車總計
    shopcart = cart_item.shopCartId
    cart_items = shopcart.cartitem_set.all()
    total_price = sum(item.sub_total for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    
    return JsonResponse({
        "quantity": cart_item.quantity,
        "sub_total": cart_item.sub_total,
        "total_price": total_price,
        "total_quantity": total_quantity
    })

def remove_item(request, item_id):
    if not request.user.is_authenticated:
        messages.error(request, "請先登入")
        return redirect("accounts:login")
        
    cart_item = get_object_or_404(CartItem, pk=item_id)
    
    # 確保用戶只能刪除自己的購物車項目
    if cart_item.shopCartId.userId != request.user:
        messages.error(request, "您沒有權限刪除此項目")
        return redirect("carts:cart")
    
    item_name = cart_item.bookId.title
    cart_item.delete()
    messages.success(request, f"{item_name} 已從購物車中移除")
    
    return redirect("carts:cart")

# 在這裡添加 JavaScript 代碼
def extra_js(request):
    return render(request, "carts/extra_js.html")