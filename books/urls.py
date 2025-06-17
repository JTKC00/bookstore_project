from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('books/', views.books, name='books'),
    path('<int:book_id>/', views.book, name='book'),
    path('search/', views.search, name='search'),
    path('hots/', views.hots, name='hots'),
]