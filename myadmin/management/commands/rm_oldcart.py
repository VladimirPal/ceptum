from django.core.management.base import BaseCommand
from cart.models import Client, CartProduct, CartItem

class Command(BaseCommand):
    def handle(self, *args, **options):
        carts = CartItem.objects.all()
        for cart in carts:
            client = Client.objects.filter(cart=cart)
            if client:
                print "%s cart is used" % cart.id
            else:
                cartp = CartProduct.objects.filter(cartitem=cart)
                for item in cartp:
                    print "cartproduct %s is not used and delete" % item.id
                    item.delete()
                print "%s cart is not used and deleted" % cart.id
                cart.delete()

