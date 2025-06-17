from django.contrib import admin
from .models import Book
from django.db import models

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'subcategory', 'is_hots', 'is_new', 'is_recommended')
    search_fields = ('title', 'author')
    list_filter = ('category', 'subcategory', 'is_hots', 'is_new', 'is_recommended')
    ordering = ('-id','-is_hots', '-is_new', '-is_recommended', 'title')
    list_per_page = 20

admin.site.register(Book, BookAdmin)