from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from order.models import Cart, CartItem
from store.models import Product

# Create your views here.

class AddToCartView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if product.quantity <= 0:
            messages.error(request, f"The product '{product.name}' is currently out of stock.")
            return redirect('cart')

        # Retrieve or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Check if product is out of stock
        new_quantity = cart_item.quantity + 1
        if new_quantity > product.quantity:
            messages.error(request,
                           f"Cannot add more of '{product.name}' to your cart. Only {product.quantity} left in stock.")
            return redirect('cart')

        # If stock is sufficient, update the cart item quantity and save
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.save()

        messages.success(request, f"'{product.name}' has been added to your cart.")
        return redirect('cart')

class ViewCart(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            items = cart.items.all()
        else:
            items = []

        for item in items:
            item.total_price = item.product.price * item.quantity

        return render(request, 'cart.html', {
            'items': items,
        })

class UpdateCartItem(LoginRequiredMixin, View):
    login_url = '/users/login/'

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


class RemoveFromCart(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

        messages.success(request, f"{cart_item.product.name} has been removed from your cart.")
        return redirect('cart')

class CheckoutView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def get(self, request):
        return render(request, 'chackout.html')
