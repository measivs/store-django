from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def shop_list(request):
    return render(request, 'shop.html')

def shop_detail_list(request):
    return render(request, 'shop-detail.html')
