from django.contrib import admin
from carts.models import ShopCart, CartItem
from datetime import datetime
# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0 # Number of empty forms to display

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','userId', 'datetime')
    search_fields = ('id','userId__username', 'datetime')
    list_filter = ('datetime', 'userId')
    list_per_page = 20
    inlines = [CartItemInline]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','shopCartId', 'bookId', 'quantity', 'unit_price', 'sub_total')
    search_fields = ('id','bookId__title', '')
    list_per_page = 20
admin.site.register(ShopCart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
