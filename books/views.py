from django.shortcuts import render, get_object_or_404
from .models import Book
from django.contrib import messages
# Create your views here.

def books(request):
    categories = {
        '文學': ['中國文學', '西方文學', '亞洲文學', '其他文學'],
        '社會科學': ['心理學', '社會學', '政治學', '法律', '其他社會科學'],
        '商業財經': ['投資理財', '商業管理', '市場營銷', '會計財務', '經濟學', '其他商業財經'],
        '飲食文化': ['烹飪', '飲品', '飲食歷史', '其他飲食文化'],
        '心理勵志': ['自我提升', '成功學', '心靈雞湯', '其他心理勵志'],
        '其他':['其他']
    }
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    books = Book.objects.all()
    if category:
        try:
            books = books.filter(category=category)
        except ValueError:
            messages.error(request, '無效的類別。')
    if subcategory:
        try:
            books = books.filter(subcategory=subcategory)
        except ValueError:
            messages.error(request, '無效的子類別。')
    return render(request, 'books/categories.html', {
        'categories': categories,
        'books': books,
        'selected_category': category,
        'selected_subcategory': subcategory,
    })

def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book.html', {
        'book': book
    })

def search(request):
    return render(request, 'books/search.html')

def hots(request):
    category = request.GET.get('category', 'hots')
    books = Book.objects.all()
    if category == 'hots':
        books = books.filter(is_hots=True)
        category_name = '熱買推薦'
    elif category == 'newbook':
        books = books.filter(is_new=True)
        category_name = '新書上架'
    elif category == 'recommend':
        books = books.filter(is_recommended=True)
        category_name = '精選推薦'
    else:
        books = []
        category_name = ''
    categories = [
        ('hots', '熱買推薦'),
        ('newbook', '新書上架'),
        ('recommend', '精選推薦'),
    ]
    return render(request, 'books/hots.html', {
        'categories': categories,
        'books': books,
        'selected_category': category,
        'category_name': category_name,
    })