from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用戶")
    last_name = models.CharField("姓氏", max_length=100, blank=False, null=False)
    first_name = models.CharField("名字", max_length=100, blank=False, null=False)
    email = models.EmailField("電郵", blank=False, null=False)
    message = models.TextField("查詢內容")
    created_at = models.DateTimeField("提交時間", auto_now_add=True)
    phone = models.CharField("聯絡電話", max_length=15, blank=True, null=True)

    def __str__(self):  
        if self.user:
            return f"{self.user.username} 的查詢"
        return f"{self.first_name} {self.last_name}  的查詢"
