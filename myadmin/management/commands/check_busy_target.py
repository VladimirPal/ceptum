# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from myadmin.models import Target
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.datetime.today()
        targets = Target.objects.filter(is_busy=True, callback=False).exclude(is_busy_at__range=[now - datetime.timedelta(hours=2), now])
        for target in targets:
            target.is_busy = False
            target.is_busy_at = None
            target.save()
