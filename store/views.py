from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from store.models import Product, Category
from django.db.models import Count

# Create your views here.
def home(request):
    parent_categories = Category.objects.filter(parent__isnull=True)

    fruits_category = Category.objects.filter(category_name='fruits').first()
    fruits_products = Product.objects.none()
    if fruits_category:
        fruits_products = Product.objects.filter(category__in=fruits_category.get_children())

    vegetables_category = Category.objects.filter(category_name='vegetables').first()
    vegetables_products = Product.objects.none()
    if vegetables_category:
        vegetables_products = Product.objects.filter(category__in=vegetables_category.get_children())

    context = {
        'parent_categories': parent_categories,
        'fruits_products': fruits_products,
        'vegetables_products': vegetables_products,
    }

    return render(request, 'index.html', context=context)

def category_list(request, slug=None):
    products = None

    if slug:
        categories = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=categories)
    else:
        products = Product.objects.all()

    subcategories = Category.objects.filter(parent__isnull=False).annotate(product_count=Count('products'))

    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'subcategories': subcategories,
        'page_obj': page_obj,
        'products': products,
        'all_products_count': Product.objects.count()
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
