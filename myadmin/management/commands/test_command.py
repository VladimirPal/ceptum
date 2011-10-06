          # -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from catalog.models import Product, Category, CameraProduct, CategoryProduct, Feature

class Command(BaseCommand):
    def handle(self, *args, **options):
        category = Category.objects.get(slug='indoor')
        products = category.product_set.all()

        for product in products:
            camproduct = CameraProduct()
            camproduct.name = product.name
            camproduct.slug = product.slug
            camproduct.price = product.price
            camproduct.wholesale_price = product.wholesale_price
            camproduct.quantity = product.quantity
            camproduct.mini_html_description = product.mini_html_description
            camproduct.html_description = product.html_description
            camproduct.tech_details = product.tech_details
            camproduct.thumbnail_image = product.thumbnail_image
            camproduct.is_active = product.is_active
            camproduct.in_stock = product.in_stock
            camproduct.is_discount = product.is_discount
            camproduct.created_at = product.created_at
            camproduct.updated_at = product.updated_at
            all_cats = list(product.categoryproduct_set.all())
            product.delete()
            camproduct.save()
            for i in all_cats:
                m1 = CategoryProduct(category = i.category, product = camproduct, sort_number = i.sort_number)
                m1.save()
            camproduct.save()
#            product.delete()

