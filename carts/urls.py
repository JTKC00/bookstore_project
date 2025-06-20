from django.urls import path
from . import views

app_name = "carts"
urlpatterns = [
    path("cart/", views.cart, name="carts"),
]
