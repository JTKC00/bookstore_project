from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import Profile

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, "You are now logged in !")
            return redirect("pages:frontpage")
        else:
            messages.error(request, "Invalid credentials !")
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
                messages.error(request, "Username already exists !")
                return redirect("accounts:register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already used !")
                    return redirect("accounts:register")
                else:
                    user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name,last_name=last_name)
                    profile = user.profile
                    profile.phone = phone
                    profile.favour_category = favour_category
                    profile.reg_address = reg_address
                    profile.save()
                    auth.login(request, user)
                    return redirect("accounts:register")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("accounts:register")
    else:
        return render(request, 'accounts/register.html')

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.save()
        profile.phone = request.POST.get('phone')
        profile.favour_category = request.POST.get('favour_category')
        profile.reg_address = request.POST.get('reg_address')

        profile.save()
        return redirect("accounts:profile")
    return render(request, 'accounts/profile.html', {
        'user':request.user,
        'profile': profile
    })

    return render(request, 'accounts/profile.html')
