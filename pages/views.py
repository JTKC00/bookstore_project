from django.shortcuts import render

# Create your views here.
def frontpage (request):
    return render(request, 'pages/frontpage.html')
def about (request):
    return render(request, 'pages/about.html')
def contact (request):
    return render(request, 'pages/contact.html')
def privacy (request):
    return render(request, 'pages/privacy.html')