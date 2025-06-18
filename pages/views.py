from django.shortcuts import render
from books.models import Book

# Create your views here.
#呢個 view 會搵出 5 本被標記為熱門（hots=True）嘅書本。
#用 render 將書本資料傳去 frontpage.html template，變成 books 變數。
def frontpage (request):
    books = Book.objects.filter(is_recommended=True)[:5]  # 取5本推薦書
    return render(request, 'pages/frontpage.html',{'books':books})

def about (request):
    return render(request, 'pages/about.html')
def contact (request):
    return render(request, 'pages/contact.html')
def privacy (request):
    return render(request, 'pages/privacy.html')