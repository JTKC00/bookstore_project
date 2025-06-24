from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import Profile

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


# Create your views here.
def user_login(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "reset_password":
            return redirect("accounts:reset_password") 
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, f"{user.username}，歡迎再次光臨，祝購物愉快！")
            return redirect("pages:frontpage")
        else:
            messages.error(request, "登入有誤，請重試")
            return redirect('accounts:login')
    else:
        return render(request,'accounts/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        favour_category = request.POST.get('favour_category')
        reg_address = request.POST.get('address')
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "用戶名已被使用 !")
                return redirect("accounts:register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "電郵已被使用 !")
                    return redirect("accounts:register")
                else:
                    user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name,last_name=last_name)
                    profile = user.profile
                    profile.phone = phone
                    profile.favour_category = favour_category
                    profile.reg_address = reg_address
                    profile.save()
                    auth.login(request, user)
                    return render("pages/frontpage.html",)
        else:
            messages.error(request, "密碼與確認密碼不一致")
            return redirect("accounts:register")
    else:
        return render(request, 'accounts/register.html')
    
    
def reset_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            messages.error(request, "用戶名稱與電郵不匹配")
            return redirect("accounts:reset_password")

        # 產生 token 與 UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # ✅ 使用 reverse() 安全地產生 URL
        reset_url = reverse("accounts:password_reset_confirm", kwargs={
            "uidb64": uid,
            "token": token
        })
        reset_link = request.build_absolute_uri(reset_url)

        # 寄送 email
        subject = "重設密碼連結"
        message = f"""親愛的 {user.username}，您好：

請點擊以下連結以重設您的密碼：EMAIL_HOST_USER
{reset_link}

如果您沒有提出重設密碼的請求，請忽略此信件。
"""
        DEFAULT_FROM_EMAIL = f"開心書店 <{settings.EMAIL_HOST_USER}>"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        messages.success(request, "重設密碼連結已寄出，請檢查你的電郵。")
        return redirect("pages:frontpage")

    return render(request, "accounts/reset_password.html")

def password_reset_confirm(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            new_password2 = request.POST.get("new_password2")
            if new_password == new_password2:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "密碼已成功重設，請重新登入")
                return redirect("accounts:login")
            else:
                messages.error(request, "密碼不一致，請重新輸入")
        return render(request, "accounts/password_reset_confirm.html")
    else:
        messages.error(request, "連結無效或已過期")
        return redirect("accounts:reset_password")
    

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        action = request.POST.get("action")
        if action == "change_password":
            return redirect("accounts:change_password") 
        if action == "profile_edit":
            request.user.email = request.POST.get('email')
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            profile.phone = request.POST.get('phone')
            profile.favour_category = request.POST.get('favour_category')
            profile.reg_address = request.POST.get('reg_address')
            profile.save()
            messages.success(request, "你的資料已更新成功")           
            return redirect("pages:frontpage")
        elif action == "reset_password":
            return redirect("accounts:reset_password")
    return render(request, 'accounts/profile.html', {
        'user':request.user,
        'profile': profile
    })

@login_required
def change_password(request):
    if request.method =='POST':
        action = request.POST.get("action")
        if action == "giveup":
            return redirect("pages:frontpage")   
        else:        
            old_password = request.POST.get('old_password')
            if not request.user.check_password(old_password):
                messages.error(request, "舊密碼不正確")
                return redirect('accounts:change_password')
            else:
                new_password = request.POST.get('new_password')
                new_password2 = request.POST.get('new_password2')
                if new_password != new_password2:
                    messages.error(request, "新密碼與確認密碼不一致")
                    return redirect('accounts:change_password')

                if old_password == new_password:
                    messages.warning(request, "新密碼不可與舊密碼相同。")
                    return redirect('accounts:change_password')
                request.user.set_password(new_password)
                request.user.save()       
                    # 確保用戶不會被登出（密碼變了）
                update_session_auth_hash(request, request.user)
                messages.success(request, "密碼更改成功！")
                return redirect('pages:frontpage')         
    return render(request, 'accounts/change_password.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "登出成功，歡迎再次光臨！")
    return redirect("pages:frontpage")