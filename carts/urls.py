from django.urls import path, include
from .views import cart
from . import views
app_name = 'carts'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
]