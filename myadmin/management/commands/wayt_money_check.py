from django.core.management.base import BaseCommand
from cart.models import Client, CartProduct
from myadmin.models import Waytmoney

class Command(BaseCommand):
    def handle(self, *args, **options):
            clients_wayt_money = Client.objects.exclude(status='CASH_IN').exclude(status='REFUSED').exclude(status='CONTACT_AT').exclude(status='BACK').exclude(status='CHANGE').exclude(status='WAYT_PRODUCT').exclude(status='COURIER_TAKE').exclude(status='COURIER_SEND').exclude(status='POSTSEND').exclude(status='PROCESS')
            money = 0
            for client in clients_wayt_money:
                products = CartProduct.objects.filter(cartitem=client.cart_id)
                for product in products:
                    money += product.product.price * product.quantity
            wayt_money = Waytmoney.objects.get(id=1)
            wayt_money.wayt_money = money
            wayt_money.save()
