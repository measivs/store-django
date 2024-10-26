from django.urls import path
from store import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/', views.CategoryProductListView.as_view(), name='main_category'),
    path('category/<slug:slug>/', views.CategoryProductListView.as_view(), name='category'),
    path('product/<slug:slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]