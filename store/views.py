from django.shortcuts import render

from store.models import Product, Category


# Create your views here.

def home(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    fruits_category = Category.objects.get(category_name='fruits')
    fruits_products = Product.objects.filter(category__in=fruits_category.get_children())
    vegetables_category = Category.objects.get(category_name='vegetables')
    vegetables_products = Product.objects.filter(category__in=vegetables_category.get_children())
    context = {'parent_categories': parent_categories,
               'fruits_products': fruits_products,
               'vegetables_products': vegetables_products,}

    return render(request, 'index.html', context=context)

def category_list(request, slug):
    all_products = Product.objects.all()
    subcategories = Category.objects.filter(parent__isnull=False)
    context = {'products': all_products,
               'subcategories': subcategories,
                }

    return render(request, 'shop.html', context=context)

def product_detail(request, slug):
    return render(request, 'shop-detail.html')

def contact(request):
    return render(request, 'contact.html')
