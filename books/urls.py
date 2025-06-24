from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('<int:book_id>/', views.book, name='book'),
    path('search/', views.search, name='search'),
    path('hots/', views.hots, name='hots'),
    path('fastapi-search/', views.fastapi_search, name='fastapi_search'),
]