from django.shortcuts import get_object_or_404, render
from books.models import Book
from django.contrib.auth.models import User
from .models import ShopCart, CartItem

# Create your views here.
def cart(request):
    # Get Shopcart parameter
    user = request.user
    shop_cart, created = ShopCart.objects.get_or_create(userId=user)
    cart_items = CartItem.objects.filter(shopCartId=shop_cart)
    total = sum(item.unit_price * item.quantity for item in cart_items)
    context = {"shop_cart":shop_cart, "cart_items":cart_items, "total": total}
    print("user",user.id)
    return render(request, 'carts/cart.html', context)

def add_to_cart(request):
    if request.method == 'GET':
        book_id = request.GET.get('book.id')
        book = get_object_or_404(Book, pk=book_id)
        # user = User.objects.get(pk=1)  # user is a User instance
        user = request.user
        shop_cart, created = ShopCart.objects.get_or_create(userId=user) #assign a User instance to a ForeignKey field (userId),

        unit_price = book.price
        # Get quantity from form
        try:
            quantity = int(request.GET.get('quantity', 1)) # Currently use GET not POST
            print("quantity",quantity)
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1
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