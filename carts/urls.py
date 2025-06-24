from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    # 現在匹配 /carts/cart/
    path('cart/', views.cart, name='cart'),
    path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    # 添加這兩個 URL 路徑來處理新增的功能
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
]
