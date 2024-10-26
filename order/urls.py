from django.urls import path
from order import views

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update-cart-item/<int:item_id>/', views.UpdateCartItem.as_view(), name='update_cart_item'),
    path('remove-from-cart/<int:item_id>/', views.RemoveFromCart.as_view(), name='remove_from_cart'),
    path('cart/', views.ViewCart.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]