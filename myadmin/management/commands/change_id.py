# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from myadmin.models import Target, Phone

class Command(BaseCommand):
    def handle(self, *args, **options):
        phones = Phone.objects.all()
        i = 1067
        for phone in phones:
            new_phone = phone
            phone.delete()
            new_phone.id = i
            new_phone.save()
            i += 1
