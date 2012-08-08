# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from myadmin.models import Target

class Command(BaseCommand):
    def handle(self, *args, **options):
        targets = Target.objects.filter(user_id=8).exclude(is_positive=1)
        for target in targets:
            target.fail_reason = None
            target.is_busy = 0
            target.is_busy_at = None
            target.is_done = 0
            target.callback = 0
            target.callback_at = None
            target.done_at = None
            target.notavailable_count = 0
            target.notavailable_date = None
            target.client = None
            target.user = None
            print target.id
            target.save()

