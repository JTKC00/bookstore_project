from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order, OrderItem
from datetime import datetime
from carts.models import ShopCart, CartItem


# Create your views here.
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

    #    shop_cart = ShopCart.objects.filter(userId=user).("")
    #       userid =
    #       shopCartId =

    #    Invoice_no = ShopCart.shopCartId


#    return render(
#        request,
#        "orders/orderconfirm.html",
#        {
#            "receipient": receipient,
#            "receipient_phone": receipient_phone,
#            "shipping_address": shipping_address,
#        },
#    )


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
