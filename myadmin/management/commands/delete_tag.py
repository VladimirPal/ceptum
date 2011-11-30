          # -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import re
from django.utils.encoding import smart_unicode, smart_str
from catalog.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        p = re.compile('<div id="-chrome-auto-translate-plugin-dialog".*</div>',re.DOTALL)
        products = Product.objects.all()

        for product in products:
            mini_html_descr = smart_str(product.tech_details)
            m = p.sub('',mini_html_descr)
            print m
            product.tech_details = m
            product.save()
