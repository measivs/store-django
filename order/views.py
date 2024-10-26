from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from order.models import Cart, CartItem
from store.models import Product

# Create your views here.

class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        # Retrieve or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Check if product is out of stock
        new_quantity = cart_item.quantity + 1
        if new_quantity > product.quantity or product.quantity <= 0:
            # If the new quantity exceeds available stock, show an error message
            messages.error(request, f"The product '{product.name}' is currently out of stock.")
            return redirect('cart')

        # If stock is sufficient, update the cart item quantity and save
        cart_item.quantity = new_quantity
        cart_item.save()

        messages.success(request, f"'{product.name}' has been added to your cart.")
        return redirect('cart')

class ViewCart(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            items = cart.items.all()
        else:
            items = []

        for item in items:
            item.total_price = item.product.price * item.quantity

        total_items = sum(item.quantity for item in items)

        return render(request, 'cart.html', {
            'items': items,
            'total_items': total_items,
        })

class UpdateCartItem(View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        requested_quantity = int(request.POST.get('quantity', 0))
        product = get_object_or_404(Product, id=item.product.id)

        if requested_quantity > product.quantity:
            messages.error(request, f"Insufficient stock for {product.name}. Only {product.quantity} available.")
            return redirect('cart')

        item.quantity = requested_quantity
        item.save()

        messages.success(request, f"{item.product.name} quantity updated to {requested_quantity}.")
        return redirect('cart')


class RemoveFromCart(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

        messages.success(request, f"{cart_item.product.name} has been removed from your cart.")
        return redirect('cart')

class CheckoutView(View):
    def get(self, request):
        return render(request, 'chackout.html')
