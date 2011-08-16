from django.core.management.base import BaseCommand
from cart.models import Client
import urllib

class Command(BaseCommand):
    def handle(self, *args, **options):
        clients = Client.objects.all()
        for client in clients:
            if client.referrer:
                print len(str(client.referrer))
                print urllib.unquote(client.referrer.encode('utf8'))