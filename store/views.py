from itertools import product
from lib2to3.fixes.fix_input import context
from django.shortcuts import render, get_object_or_404
from unicodedata import category

from store.models import Product, Category
from django.db.models import Count

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

def category_list(request, slug=None):
    categories = None
    products = None
    if slug:
        categories = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=categories)
    else:
        products = Product.objects.all()

    # all_products = Product.objects.all()
    subcategories = Category.objects.filter(parent__isnull=False).annotate(product_count=Count('products'))
    context = {'products': products,
               'subcategories': subcategories,
                }

    return render(request, 'shop.html', context=context)

def product_detail(request, slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {'single_product': single_product}

    return render(request, 'shop-detail.html', context=context)

def contact(request):
    return render(request, 'contact.html')
