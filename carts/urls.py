from django.urls import path
from .views import cart
from . import views
app_name = 'carts'
urlpatterns = [
    path('cart_item', cart, name=''),
    path('add-to-cart/<int:book_id>', views.add_to_cart, name='add_to_cart'),
]