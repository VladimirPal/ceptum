          # -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from myadmin.models import Target, Phone

class Command(BaseCommand):
    def handle(self, *args, **options):
        targets = Target.objects.filter(category_id=1)
        for target in targets:
            try:
                Phone.objects.get(target=target).delete()
            except :
                pass
            target.delete()
