from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_edit, name='profile_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>/', 
         views.password_reset_confirm, 
         name='password_reset_confirm'),
    path('logout/', views.logout, name='logout'),

]
