from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from order.models import Cart, CartItem
from store.models import Product

# Create your views here.

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.quantity <= 0:
        messages.error(request, f"The product {product.name} is currently out of stock.")
        return redirect('cart')

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()

    return redirect('cart')

def view_cart(request):
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


def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    requested_quantity = int(request.POST.get('quantity', 0))
    product = get_object_or_404(Product, id=item.product.id)

    if requested_quantity > product.quantity:
        messages.error(request, f"Insufficient stock for {product.name}. Only {product.quantity} available.")
        return redirect('cart')

    item.quantity = requested_quantity
    item.save()

    return redirect('cart')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    return redirect('cart')

def checkout(request):
    return render(request, 'chackout.html')
