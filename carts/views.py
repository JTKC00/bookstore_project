from django.shortcuts import get_object_or_404, render
from books.models import Book
from django.contrib.auth.models import User
from .models import ShopCart, CartItem

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