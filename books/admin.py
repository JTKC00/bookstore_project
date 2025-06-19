from django.contrib import admin
from .models import Book
from import_export import resources, fields # 用於定義匯入/匯出資源的類別
from import_export.admin import ImportExportModelAdmin # 用於匯入/匯出功能
import os # 用於遞迴搜尋檔案
from django.conf import settings # 用於獲取 MEDIA_ROOT 路徑
from django.core.files import File # 用於處理檔案儲存

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        import_id_fields = ('isbn',)  # 以 isbn 作唯一識別
        fields = ('isbn', 'title', 'author', 'publisher', 'introduction', 'category', 'subcategory', 'language', 'price', 'stock', 'is_hots', 'is_new', 'is_recommended') # 指定需要匯入/匯出的欄位

def auto_import_photos_all(modeladmin, request, queryset):
    """
    遞迴搜尋 media 內所有 jpg 及 webp，根據 ISBN 自動配對書本大圖及小圖
    """
    matched_large = 0 # 計算配對到的大圖數量
    matched_small = 0 # 計算配對到的小圖數量
    for book in queryset:
        # 配對大圖
        possible_large = [
            f"{book.isbn}_large.jpg",
            f"{book.isbn}_large.JPG",
        ]
        found_large = False # 標記是否找到大圖
        for root, dirs, files in os.walk(settings.MEDIA_ROOT): 
            for fname in files:
                if fname in possible_large or fname.startswith(f"{book.isbn}_large"):
                    photo_path = os.path.join(root, fname)
                    # 先刪除舊有相片
                    if book.photo_large:
                        book.photo_large.delete(save=False)
                    with open(photo_path, 'rb') as f:
                        book.photo_large.save(fname, File(f), save=True)
                        matched_large += 1
                        found_large = True
                        break
        if found_large:
            break
        # 如果沒有找到大圖，則不處理小圖

        # 配對小圖（支援 .jpg、.JPG、.jpg.webp、.JPG.webp）
        possible_small = [
            f"{book.isbn}_small.jpg",
            f"{book.isbn}_small.JPG",
            f"{book.isbn}_small.jpg.webp",
            f"{book.isbn}_small.JPG.webp",
        ]
        found_small = False
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for fname in files:
                if (
                    fname in possible_small
                    or fname.startswith(f"{book.isbn}_small")
                ):
                    photo_path = os.path.join(root, fname)
                    # 先刪除舊有相片
                    if book.photo_small:
                        book.photo_small.delete(save=False)
                    with open(photo_path, 'rb') as f:
                        book.photo_small.save(fname, File(f), save=True)
                        matched_small += 1
                        found_small = True
                        break
        if found_small:
            break
    # 在管理後台顯示配對結果

    modeladmin.message_user(
        request,
        f"已自動配對 {matched_large} 本書的大圖及 {matched_small} 本書的小圖。"
    )
auto_import_photos_all.short_description = "自動根據ISBN遞迴匯入大圖及小圖"


# 在 BookAdmin actions 加入
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_display = ('title', 'author', 'category', 'subcategory', 'is_hots', 'is_new', 'is_recommended') # 定義列表顯示的欄位
    search_fields = ('title', 'author') # 定義可搜尋的欄位
    list_filter = ('category', 'subcategory', 'is_hots', 'is_new', 'is_recommended')# 定義篩選器
    ordering = ('-id','-is_hots', '-is_new', '-is_recommended', 'title')# 定義排序方式
    list_per_page = 20 # 每頁顯示的書籍數量
    actions = [auto_import_photos_all] # 自動匯入相片的動作

admin.site.register(Book, BookAdmin)

# import_export 功能需要安裝 django-import-export 套件
# 確保在 settings.py 中已經添加了 'import_export' 到 INSTALLED_APPS
# 這樣就可以在 Django 管理後台中使用匯入/匯出功能了

#1. 將所有相片（如 9789620455742_large.jpg、9789620455742_small.jpg.webp 等）放入 media 目錄下任何子資料夾（例如 media/photos/2025/06/18/）。
# 2. 登入 Django 管理後台（/admin），進入「書本」(Book) 列表。
# 3. 勾選你想自動配對相片的書本（可全選）。
# 4. 在上方「動作」(Actions) 下拉選單選擇「自動根據ISBN遞迴匯入大圖及小圖」。
# 5. 按「執行」(Go)。