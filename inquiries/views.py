from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactMessageForm
from django.utils import timezone
from datetime import timedelta

def inquiries(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, user=request.user)
        if form.is_valid():
            # 檢查是否在短時間內有重複提交
            user_email = form.cleaned_data['email']
            user_message = form.cleaned_data['message']
            recent_time = timezone.now() - timedelta(minutes=5)
            
            # 檢查重複提交
            duplicate = ContactMessage.objects.filter(
                email=user_email,
                message=user_message,
                created_at__gte=recent_time
            ).exists()
            
            if duplicate:
                messages.warning(request, "您的查詢已提交，請勿重複發送。")
                return redirect('/')
                
            # 正常保存
            contact_message = form.save(commit=False)
            if request.user.is_authenticated:
                contact_message.user = request.user
                
            contact_message.save()
            messages.success(request, "您的查詢已成功送出，我們會盡快回覆您！")
            return redirect('/')
    else:
        form = ContactMessageForm(user=request.user)
    
    # 添加模板路徑
    return render(request, 'Inquiries/inquiry_form.html', {'form': form})
