from django.shortcuts import render


# Create your views here.
def shipping(request):
    return render(request, "orders/shipping.html")


def orderconfirm(request):
    return render(request, "orders/orderconfirm.html")
