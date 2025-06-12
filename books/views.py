from django.shortcuts import render

# Create your views here.
def books(request):
    return render(request, 'books/books.html')
def book(request, book_id):
    return render(request, 'books/book.html')
def search(request):
    return render(request, 'books/search.html')