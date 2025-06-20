from .models import Profile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
# Register your models here.
