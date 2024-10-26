from .models import Cart

def cart_items(request):
    total_items = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_items = sum(item.quantity for item in cart.items.all())

    return {
        'total_items': total_items,
    }
