from django .urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('books', views.books, name='books'),
    path('book', views.book, name='book'),
    path('search', views.search, name='search'),
]