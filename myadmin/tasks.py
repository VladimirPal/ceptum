# -*- coding: utf-8 -*-
from celery.task import task
from myadmin.models import Target
import datetime
from django.conf import settings
from django.core.mail.message import EmailMessage

@task(name="check_busy_target")
def check_busy_target():
    now = datetime.datetime.today()
    targets = Target.objects.filter(is_busy=True).exclude(is_busy_at__range=[now - datetime.timedelta(hours=2), now])
    for target in targets:
        target.is_busy = False
        target.is_busy_at = None
        target.save()

@task(name="send_mail")
def send_mail(user, title, body, to, is_attach, attach):
    msg = EmailMessage(title, body, user.email, [to,])
    print attach
    if not is_attach:
        msg.attach_file('./media/'+ attach)
    msg.send()
