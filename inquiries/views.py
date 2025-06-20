from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactMessageForm

def inquiries(request):
    if request.method == 'POST':
        # 創建表單時傳入用戶參數
        form = ContactMessageForm(request.POST, user=request.user)
        if form.is_valid():
            contact_message = form.save(commit=False)
            
            # 明確關聯當前登入用戶
            if request.user.is_authenticated:
                contact_message.user = request.user
                
            contact_message.save()
            messages.success(request, "您的查詢已成功送出，我們會盡快回覆您！")
            return redirect('/')
    else:
        # GET 請求也傳入用戶參數
        form = ContactMessageForm(user=request.user)
    
    return render(request, 'Inquiries/inquiry_form.html', {'form': form})
