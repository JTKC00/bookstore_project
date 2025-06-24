from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from carts.models import ShopCart, CartItem
from django.contrib import messages
from datetime import datetime


def shipping(request):

    shopcart_id = request.GET.get("shopcart_id")
    total_amount = request.GET.get("total_amount")
    total_quantity = request.GET.get("total_quantity")

    shopcart = get_object_or_404(ShopCart, id=shopcart_id, userId=request.user)
    cart_items = shopcart.cartitem_set.all()

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


def orderinfo(request):
    if not request.user.is_authenticated:
        messages.error(request, "請先登入")
        return redirect("accounts:login")

    # Get all orders for this user
    orders = Order.objects.filter(userId=request.user).order_by("-order_date")

    # Get selected order (by invoice_no or order id)
    selected_order = None
    order_items = []
    total_quantity = 0
    total_amount = 0

    order_id = request.GET.get("order_id")
    if order_id:
        selected_order = get_object_or_404(Order, id=order_id, userId=request.user)
        order_items = OrderItem.objects.filter(orderid=selected_order)
        total_quantity = sum(item.quantity for item in order_items)
        total_amount = selected_order.total_amount

    return render(
        request,
        "orders/orderinfo.html",
        {
            "orders": orders,
            "selected_order": selected_order,
            "order_items": order_items,
            "total_quantity": total_quantity,
            "total_amount": total_amount,
        },
    )


def orderconfirm(request):
    if request.method == "POST":
        shopcart_id = request.POST.get("shopcart_id")
        total_amount = request.POST.get("total_amount")
        total_quantity = request.POST.get("total_quantity")
        receipient = request.POST.get("receipient")
        receipient_phone = request.POST.get("receipient_phone")
        shipping_address = request.POST.get("shipping_address")

        shopcart = get_object_or_404(ShopCart, id=shopcart_id, userId=request.user)
        cart_items = shopcart.cartitem_set.all()

        # Check if an order already exists for this cart and user
        order = Order.objects.filter(shopCartId=shopcart, userId=request.user).first()
        if order:
            # If order exists, just show the confirmation page with existing order and items
            order_items = OrderItem.objects.filter(orderid=order)
            messages.warning(request, "The order is already made")
            return render(
                request,
                "orders/orderconfirm.html",
                {
                    "order": order,
                    "cart_items": order_items,
                    "total_quantity": total_quantity,
                    "total_amount": total_amount,
                    "shopcart": shopcart,
                    #                    "already_submitted": True,
                },
            )

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


def create_order(request):
    if not request.user.is_authenticated:
        messages.error(request, "請先登入")
        return redirect("accounts:login")

    shopcart = get_object_or_404(ShopCart, userId=request.user)
    cart_items = shopcart.cartitem_set.all()

    # 防止重覆：檢查這個購物車是否已建立訂單且未取消
    existing_order = Order.objects.filter(
        shopcart=shopcart, status__in=["pending", "paid"]
    ).first()
    if existing_order:
        messages.warning(request, "此購物車已建立訂單，請勿重覆下單。")
        return redirect("orders:orderconfirm", order_id=existing_order.id)

    # 建立訂單
    order = Order.objects.create(
        user=request.user,
        shopcart=shopcart,
        total_amount=sum(item.sub_total for item in cart_items),
        status="pending",
    )
    # 建立訂單明細
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.bookId,
            quantity=item.quantity,
            unit_price=item.unit_price,
            sub_total=item.sub_total,
        )
    # 建立訂單成功後，清空購物車
    shopcart.cartitem_set.all().delete()
    # 或者：shopcart.delete()  # 如果你想連購物車本身都刪除
    messages.success(request, "訂單已建立，購物車已清空。")
    return redirect("orders:orderconfirm", order_id=order.id)
