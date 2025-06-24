from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from carts.models import ShopCart, CartItem
from django.contrib import messages
from datetime import datetime


@login_required
def shipping(request):

    shopcart_id = request.GET.get("shopcart_id")
    total_amount = request.GET.get("total_amount")
    total_quantity = request.GET.get("total_quantity")

    shopcart = get_object_or_404(ShopCart, id=shopcart_id, userId=request.user)
    cart_items = shopcart.cartitem_set.filter(is_ordered=False)

    return render(
        request,    
        "orders/shipping.html",
        {
            "shopcart": shopcart,
            "cart_items": cart_items,
            "total_quantity": total_quantity,
            "total_amount": total_amount,
        },
    )


@login_required
def orderconfirm(request):
    if request.method == "POST":
        shopcart_id = request.POST.get("shopcart_id")
        total_amount = request.POST.get("total_amount")
        total_quantity = request.POST.get("total_quantity")
        receipient = request.POST.get("receipient")
        receipient_phone = request.POST.get("receipient_phone")
        shipping_address = request.POST.get("shipping_address")

        shopcart = get_object_or_404(ShopCart, id=shopcart_id, userId=request.user)
        cart_items = shopcart.cartitem_set.filter(is_ordered=False)

        # 檢查是否已經有未付款的訂單（避免重複創建）
        pending_order = Order.objects.filter(
            shopCartId=shopcart, 
            userId=request.user, 
            payment_status="PENDI"
        ).first()
        
        if pending_order:
            # 檢查該訂單的商品是否與當前購物車一致
            order_items = OrderItem.objects.filter(orderid=pending_order)
            cart_items_ids = set(cart_items.values_list('id', flat=True))
            order_cart_ids = set(order_items.values_list('CartID__id', flat=True))
            
            # 如果訂單商品與購物車商品一致，則顯示現有訂單
            if cart_items_ids == order_cart_ids and cart_items.exists():
                return render(
                    request,
                    "orders/orderconfirm.html",
                    {
                        "order": pending_order,
                        "cart_items": order_items,
                        "total_quantity": total_quantity,
                        "total_amount": total_amount,
                        "shopcart": shopcart,
                    },
                )
            else:
                # 如果購物車已改變，刪除舊訂單重新創建
                pending_order.delete()

        # 在創建訂單前檢查所有商品庫存
        stock_errors = []
        for item in cart_items:
            if item.quantity > item.bookId.stock:
                stock_errors.append(
                    f"{item.bookId.title}：需要 {item.quantity} 本，但庫存只有 {item.bookId.stock} 本"
                )
        
        if stock_errors:
            for error in stock_errors:
                messages.error(request, error)
            messages.error(request, "請調整購物車中的商品數量後再試。")
            return redirect("carts:cart")

        # Otherwise, create a new order and order items
        order = Order.objects.create(
            userId=request.user,
            shopCartId=shopcart,
            invoice_no=shopcart_id,
            order_date=datetime.now(),
            receipient=receipient,
            receipient_phone=receipient_phone,
            shipping_address=shipping_address,
            payment_status="PENDI",
            shipping_status="STOCK",
            total_amount=total_amount,
        )

        for item in cart_items:
            OrderItem.objects.create(
                bookid=item.bookId,
                CartID=item,
                orderid=order,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subTotal=item.quantity * item.unit_price,
            )

        return render(
            request,
            "orders/orderconfirm.html",
            {
                "order": order,
                "cart_items": cart_items,
                "total_quantity": total_quantity,
                "total_amount": total_amount,
                "shopcart": shopcart,
            },
        )
    else:
        return redirect("orders:shipping")


@login_required
def create_order(request):
    if not request.user.is_authenticated:
        messages.error(request, "請先登入")
        return redirect('accounts:login')

    shopcart = get_object_or_404(ShopCart, userId=request.user)
    cart_items = shopcart.cartitem_set.filter(is_ordered=False)

    # 防止重覆：檢查這個購物車是否已建立訂單且未取消
    existing_order = Order.objects.filter(shopcart=shopcart, status__in=['pending', 'paid']).first()
    if existing_order:
        messages.warning(request, "此購物車已建立訂單，請勿重覆下單。")
        return redirect('orders:orderconfirm', order_id=existing_order.id)

    # 建立訂單
    order = Order.objects.create(
        user=request.user,
        shopcart=shopcart,
        total_amount=sum(item.sub_total for item in cart_items),
        status='pending'
    )
    # 建立訂單明細
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.bookId,
            quantity=item.quantity,
            unit_price=item.unit_price,
            sub_total=item.sub_total
        )
    # 建立訂單成功後，標記購物車商品為已下單
    shopcart.cartitem_set.filter(is_ordered=False).update(is_ordered=True)
    # 或者：shopcart.delete()  # 如果你想連購物車本身都刪除
    messages.success(request, "訂單已建立，購物車已清空。")
    return redirect('orders:orderconfirm', order_id=order.id)


@login_required
def order_detail(request, order_id):
    """訂單詳情頁面"""
    order = get_object_or_404(Order, id=order_id, userId=request.user)
    order_items = OrderItem.objects.filter(orderid=order)
    
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_items': order_items,
    })


@login_required
def order_list(request):
    """用戶訂單列表頁面"""
    from django.core.paginator import Paginator
    
    orders = Order.objects.filter(userId=request.user).order_by('-order_date')
    
    # 分頁處理
    paginator = Paginator(orders, 10)  # 每頁顯示 10 個訂單
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'orders/order_list.html', {
        'orders': page_obj,
    })
