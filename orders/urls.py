from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("shipping/", views.shipping, name="shipping"),
    path("orderconfirm/", views.orderconfirm, name="orderconfirm"),
    path("orderinfo/", views.orderinfo, name="orderinfo"),
]
