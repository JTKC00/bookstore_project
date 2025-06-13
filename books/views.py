from django.shortcuts import render

# Create your views here.
def categories(request):
    return render(request, 'books/categories.html')
def book(request, book_id):
    return render(request, 'books/book.html')
def search(request):
    return render(request, 'books/search.html')
def hots(request):
    return render(request, 'books/hots.html')