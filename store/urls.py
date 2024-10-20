from itertools import product
from tkinter.font import names

from django.urls import path
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/category/<slug:slug>/', views.category_list, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
]