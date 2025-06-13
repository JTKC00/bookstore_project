from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
]
