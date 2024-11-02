from django.db.models import Min, Max
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from store.models import Product, Category, ProductTag

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        # Get all parent categories
        parent_categories = Category.objects.filter(parent__isnull=True)

        # Get fruits category and its products
        fruits_category = Category.objects.filter(category_name='fruits').first()
        fruits_products = Product.objects.none()
        if fruits_category:
            fruits_products = Product.objects.filter(category__in=fruits_category.get_children())

        # Get vegetables category and its products
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


@method_decorator(cache_page(600), name='dispatch')
class CategoryProductListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        # If a slug is provided, filter products by the category with that slug
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            queryset = Product.objects.filter(category=category)
        else:
            queryset = Product.objects.all()

        # Filter by tag if a tag is selected
        selected_tag_id = self.request.GET.get('tag')
        if selected_tag_id:
            queryset = queryset.filter(tag__id=selected_tag_id)

        # Apply search query
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(tag__name__icontains=search_query))

        # Get the minimum and maximum prices from the Product model
        min_price = int(self.request.GET.get('min_price', 0))
        max_price = int(self.request.GET.get('max_price', 500))
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        price_data = Product.objects.aggregate(Min('price'), Max('price'))

        context['product_tags'] = ProductTag.objects.all()
        context['subcategories'] = Category.objects.filter(parent__isnull=False)
        context['min_price'] = price_data['price__min'] or 0
        context['max_price'] = price_data['price__max'] or 500

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop-detail.html'
    context_object_name = 'single_product'

    def get_object(self, queryset=None):
        # Get the object based on the slugs
        slug = self.kwargs.get('slug')
        product_slug = self.kwargs.get('product_slug')
        return get_object_or_404(Product, category__slug=slug, slug=product_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
