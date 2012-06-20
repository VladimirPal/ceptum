# -*- coding: utf-8 -*-
from celery.task import task
from myadmin.models import Target
import os
import datetime
from django.conf import settings
from django.core.mail.message import EmailMessage

@task(name="check_busy_target")
def check_busy_target():
    now = datetime.datetime.today()
    targets = Target.objects.filter(is_busy=True, callback=False).exclude(is_busy_at__range=[now - datetime.timedelta(hours=2), now])
    for target in targets:
        target.is_busy = False
        target.is_busy_at = None
        target.save()

@task(name="send_mail")
def send_mail(user, title, body, to, is_attach, attach):
    settings.EMAIL_HOST_USER = user.email
    settings.EMAIL_HOST_PASSWORD = settings.USER_EMAIL_PASSWORDS[user.email]
    msg = EmailMessage(title, body, user.email, [to,])
    if attach:
        if not is_attach:
            msg.attach_file(os.path.join(settings.MEDIA_ROOT, attach))
    msg.send()
