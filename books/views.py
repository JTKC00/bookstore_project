from django.shortcuts import render, get_object_or_404
from .models import Book
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

def categories(request):
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

    # 分頁處理
    paginator = Paginator(books, 6)  # 每頁顯示 6 本書
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/categories.html', {
        'categories': categories,
        'books': page_obj,
        'selected_category': category,
        'selected_subcategory': subcategory,
    })

def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book.html', {
        'book': book
    })

def search(request):
    query = request.GET.get('q', '')           # 取得搜尋關鍵字，q 參數（通常係搜尋字），如果冇，就用預設值 ''(emtpy)
    category = request.GET.get('category', '') # 取得分類（如有）
    price = request.GET.get('price', '')       # 取得價格範圍（如有）
    books = Book.objects.all()                 # 先取出所有書
    #左邊嘅variables （自定義名稱）係從 GET 請求中取得的參數，右邊係預設值
    # 如果冇輸入關鍵字，就用所有書籍 
    # get 後面嘅tuple('xxx', '') 左邊係key名（key），右邊係預設值

    # 如果有輸入關鍵字，就用 title 或 author 做模糊搜尋
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # 如果有選分類，就 filter category
    if category:
        books = books.filter(category=category)

    # 如果有選價格範圍，就 filter price
    if price:
        if price == '0-100':
            books = books.filter(price__gte=0, price__lte=100)
        elif price == '101-200':
            books = books.filter(price__gte=101, price__lte=200)
        elif price == '201-500':
            books = books.filter(price__gte=201, price__lte=500)
        elif price == '501-':
            books = books.filter(price__gte=501)

    # 將搜尋結果傳去 template
    return render(request, 'books/search.html', {'books': books})

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