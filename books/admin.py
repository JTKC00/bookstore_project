from django.contrib import admin
from .models import Book
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        import_id_fields = ('isbn',)  # 以 isbn 作唯一識別
        fields = ('isbn', 'title', 'author', 'publisher', 'introduction', 'category', 'subcategory', 'language', 'price', 'stock', 'is_hots', 'is_new', 'is_recommended') # 指定需要匯入/匯出的欄位

class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource # 定義資源類別
    list_display = ('title', 'author', 'category', 'subcategory', 'is_hots', 'is_new', 'is_recommended') # 定義列表顯示的欄位
    search_fields = ('title', 'author') # 定義可搜尋的欄位
    list_filter = ('category', 'subcategory', 'is_hots', 'is_new', 'is_recommended')# 定義篩選器
    ordering = ('-id','-is_hots', '-is_new', '-is_recommended', 'title')# 定義排序方式
    list_per_page = 20 # 每頁顯示的書籍數量

admin.site.register(Book, BookAdmin)

# import_export 功能需要安裝 django-import-export 套件
# 確保在 settings.py 中已經添加了 'import_export' 到 INSTALLED_APPS
# 這樣就可以在 Django 管理後台中使用匯入/匯出功能了