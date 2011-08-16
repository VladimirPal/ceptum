          # -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import urllib2, re, time
from cart.models import Client

class Command(BaseCommand):
    def handle(self, *args, **options):
        clients = Client.objects.filter(status='POSTSENDED')
        for client in clients:
            if client.tracking_number:
                try:
                    response = urllib2.urlopen('http://www.emspost.ru/tracking/%s' % client.tracking_number)
                except urllib2.HTTPError:
                    time.sleep(1200)
                    continue
                result = re.findall(ur"<tr class=\"(.*)\"><td>(.+?)</tr>", response.read())
                try:
                    i = result[len(result) - 1][1]
                    a = i.split('<td>')
                    if a[4][:-5] == 'Единичный':
                        t_status = "%s %s" % (a[0][:-5], a[1][:-5])
                    elif a[4][:-5] == 'Иная':
                        t_status = "%s %s" % (a[0][:-5], a[1][:-5])
                    else:
                        t_status = "%s %s" % (a[4][:-5], a[1][:-5])
                    client.tracking_status = t_status[:-6]
                    client.save()
                    time.sleep(10)
                except :
                    pass
