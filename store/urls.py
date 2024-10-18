from itertools import product
from tkinter.font import names

from django.urls import path
from store import views

urlpatterns = [
    path('', views.home),
    path('category/<slug:slug>/', views.shop_list, name='shop'),
    path('products/<slug:slug>/', views.shop_detail_list, name='shop_detail'),
]