from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'email', 'created_at', 'user')
    list_filter = ('created_at', 'user')
    search_fields = ('last_name', 'first_name', 'email', 'message')  # 修改這裡：使用實際欄位
    raw_id_fields = ('user',)
    
    def get_name(self, obj):
        """顯示發送者名稱，優先顯示用戶名稱"""
        if obj.user:
            return f"{obj.user.username} ✓"
        return f"{obj.first_name} {obj.last_name}" if obj.first_name or obj.last_name else "匿名"  # 修改這裡
    get_name.short_description = '發送者'
    get_name.admin_order_field = 'user__username'
