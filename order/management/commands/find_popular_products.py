from django.core.management.base import BaseCommand
from order.models import CartItem
from django.db.models import Count

class Command(BaseCommand):
    help = 'Finds the top 3 most popular products from users\' carts'

    def handle(self, *args, **kwargs):
        top_products = (
            CartItem.objects
            .values('product__id', 'product__name')
            .annotate(user_count=Count('cart__user', distinct=True))
            .order_by('-user_count')
            [:3]
        )

        for index, product in enumerate(top_products, start=1):
            product_name = product['product__name']
            user_count = product['user_count']
            self.stdout.write(f"{index}. {product_name} - {user_count} users added to cart")
