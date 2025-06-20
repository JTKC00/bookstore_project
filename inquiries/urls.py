from django .urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('inquiry/', views.inquiries, name='inquiry')
]
