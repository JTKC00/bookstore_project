from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['last_name', 'first_name', 'email', 'phone', 'message']  # 移除 'user'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
        error_messages = {
            'last_name': {'required': '請輸入姓氏'},
            'first_name': {'required': '請輸入名字'},
            'email': {'required': '請輸入電郵'},
            'message': {'required': '請輸入查詢內容'},
        }
    
    def __init__(self, *args, **kwargs):
        # 從 kwargs 取出用戶
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 如果使用者已登入
        if user and user.is_authenticated:
            # 自動填充相關欄位
            self.fields['last_name'].widget = forms.HiddenInput()
            self.fields['last_name'].required = False
            self.fields['last_name'].initial = user.last_name if hasattr(user, 'last_name') else ''
            
            self.fields['first_name'].widget = forms.HiddenInput()
            self.fields['first_name'].required = False
            self.fields['first_name'].initial = user.first_name if hasattr(user, 'first_name') else user.username

            self.fields['email'].widget = forms.HiddenInput()
            self.fields['email'].required = False
            self.fields['email'].initial = user.email