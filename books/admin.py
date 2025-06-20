from django.contrib import admin
from .models import Book
from import_export import resources, fields # 用於定義匯入/匯出資源的類別
from import_export.admin import ImportExportModelAdmin # 用於匯入/匯出功能
import os # 用於遞迴搜尋檔案
from django.conf import settings # 用於獲取 MEDIA_ROOT 路徑
from django.core.files import File # 用於處理檔案儲存
from PIL import Image  # 加入 PIL 庫用於檢查圖片
import shutil  # 用於移動檔案

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        import_id_fields = ('isbn',)  # 以 isbn 作唯一識別
        fields = ('isbn', 'title', 'author', 'publisher', 'introduction', 'category', 'subcategory', 'language', 'price', 'stock', 'is_hots', 'is_new', 'is_recommended') # 指定需要匯入/匯出的欄位

def auto_import_photos_all(modeladmin, request, queryset):
    """
    遞迴搜尋 media 內所有 jpg 及 webp，根據 ISBN 自動配對書本大圖及小圖，同時刪除損壞的圖片
    """
    matched_large = 0
    matched_small = 0
    errors = 0
    corrupt_deleted = 0
    error_folder = os.path.join(settings.MEDIA_ROOT, 'error_images')
    
    # 確保錯誤圖片資料夾存在
    if not os.path.exists(error_folder):
        os.makedirs(error_folder)
    
    for book in queryset:
        # 配對大圖
        possible_large = [
            f"{book.isbn}_large.jpg",
            f"{book.isbn}_large.JPG",
        ]
        found_large = False
        for root, dirs, files in os.walk(settings.MEDIA_ROOT): 
            for fname in files:
                if fname in possible_large or fname.startswith(f"{book.isbn}_large"):
                    photo_path = os.path.join(root, fname)
                    
                    # 檢查檔案是否存在及完整
                    if not os.path.exists(photo_path):
                        continue
                    
                    # 檢查圖片是否損壞
                    try:
                        with Image.open(photo_path) as img:
                            img.verify()  # 驗證圖片完整性
                    except Exception as e:
                        # 圖片損壞，移至錯誤資料夾或刪除
                        error_path = os.path.join(error_folder, fname)
                        try:
                            shutil.move(photo_path, error_path)
                            corrupt_deleted += 1
                            print(f"已移動損壞圖片到錯誤資料夾: {fname}，錯誤: {str(e)}")
                        except:
                            try:
                                os.remove(photo_path)
                                corrupt_deleted += 1
                                print(f"已刪除損壞圖片: {fname}，錯誤: {str(e)}")
                            except:
                                pass
                        continue
                    
                    # 正常處理圖片
                    try:
                        if book.photo_large:
                            book.photo_large.delete(save=False)
                        with open(photo_path, 'rb') as f:
                            book.photo_large.save(fname, File(f), save=True)
                            matched_large += 1
                            found_large = True
                            break
                    except Exception as e:
                        errors += 1
                        print(f"錯誤處理圖片 {photo_path}: {str(e)}")
                        continue
            if found_large:
                break

        # 配對小圖（類似邏輯，但加入了圖片驗證）
        possible_small = [
            f"{book.isbn}_small.jpg",
            f"{book.isbn}_small.JPG",
            f"{book.isbn}_small.jpg.webp",
            f"{book.isbn}_small.JPG.webp",
        ]
        found_small = False
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for fname in files:
                if fname in possible_small or fname.startswith(f"{book.isbn}_small"):
                    photo_path = os.path.join(root, fname)
                    
                    # 檢查檔案是否存在及完整
                    if not os.path.exists(photo_path):
                        continue
                    
                    # 檢查圖片是否損壞
                    try:
                        # 對於 JPG/JPEG 檔案
                        if photo_path.lower().endswith(('.jpg', '.jpeg')):
                            with Image.open(photo_path) as img:
                                img.verify()
                    except Exception as e:
                        # 圖片損壞，移至錯誤資料夾或刪除
                        error_path = os.path.join(error_folder, fname)
                        try:
                            shutil.move(photo_path, error_path)
                            corrupt_deleted += 1
                            print(f"已移動損壞圖片到錯誤資料夾: {fname}，錯誤: {str(e)}")
                        except:
                            try:
                                os.remove(photo_path)
                                corrupt_deleted += 1
                                print(f"已刪除損壞圖片: {fname}，錯誤: {str(e)}")
                            except:
                                pass
                        continue
                    
                    # 正常處理圖片
                    try:
                        if book.photo_small:
                            book.photo_small.delete(save=False)
                        with open(photo_path, 'rb') as f:
                            book.photo_small.save(fname, File(f), save=True)
                            matched_small += 1
                            found_small = True
                            break
                    except Exception as e:
                        errors += 1
                        print(f"錯誤處理圖片 {photo_path}: {str(e)}")
                        continue
            if found_small:
                break

    modeladmin.message_user(
        request,
        f"已自動配對 {matched_large} 本書的大圖及 {matched_small} 本書的小圖。"
        f"處理過程中有 {errors} 個錯誤，刪除/移動了 {corrupt_deleted} 張損壞圖片。"
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