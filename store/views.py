from django.shortcuts import render

from store.models import Product, Category


# Create your views here.

def home(request):
    return render(request, 'index.html')

def category_list(request, slug):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    context = {'products': all_products,
               'categories': all_categories}

    return render(request, 'shop.html', context=context)

def product_detail(request, slug):
    return render(request, 'shop-detail.html')

def contact(request):
    return render(request, 'contact.html')
