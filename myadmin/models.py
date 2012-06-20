          # -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
import os
from django.conf import settings
from storage import OverwriteStorage

STATUS_CHOICES = (
    ('CALL', 'Созвон'),
    ('OFFER', 'Скинуть КП'),
    ('INSPECTION', 'Осмотр'),
    ('PROJECT', 'Проект'),
    ('DONE', ' Готово'),
 )

REFERRER_CHOICES = (
    ('INCOMING', 'Входящий звонок'),
    ('COLD', 'Холодные звонки'),
    ('RECOMMENDATIONS', 'Рекомендации'),
    ('PARTNER_RECOMMENDATIONS', 'Рекомендации партнеров'),
    ('SITE', ' Сайт'),
    ('OTHER', ' Другое'),
)

FAIL_REASON = (
    ('IS_INSTALL', 'Уже установлено'),
    ('DONT_NEED', 'Не требуется'),
    ('DONT_TELL', 'Не сообщили'),
    ('OFFER', 'Скинул КП'),
    ('OTHER', 'Другое'),
 )

class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_name = models.TextField()
    address = models.CharField(max_length=300, null=True)
    email = models.EmailField(max_length=100, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    status_date = models.DateField(null=True, blank=True)
    status_time = models.TimeField(null=True, blank=True)
    status_comment = models.CharField(max_length=500, blank=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    data = models.TextField(null=True)
    user = models.ForeignKey(User)
    referrer = models.CharField(max_length=50, choices=REFERRER_CHOICES)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == 'DONE':
            if not Client.objects.get(id=self.pk).status == 'DONE':
                self.status_date = datetime.date.today()
        super(Client, self).save(*args, **kwargs)


class ClientFile(models.Model):
    client = models.ForeignKey(Client)
    file = models.FileField(upload_to='./clientfiles')

class Comment(models.Model):
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

class CommentFile(models.Model):
    comment = models.ForeignKey(Comment)
    file = models.FileField(upload_to='./clientfiles')

class CategoryTarget(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

class Target(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryTarget)
    city = models.CharField(default='Москва', max_length=50, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    site = models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    fail_reason = models.CharField(null=True, blank=True, max_length=50, choices=FAIL_REASON)
    comment = models.TextField(null=True, blank=True)
    is_busy = models.BooleanField(default=False)
    is_busy_at = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    is_positive = models.BooleanField(default=False)
    client = models.ForeignKey(Client, null=True, blank=True)
    callback = models.BooleanField(default=False)
    callback_at = models.DateField(null=True, blank=True)
    notavailable_count = models.IntegerField(default=0, max_length=1)
    notavailable_date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    done_at = models.DateField(null=True, blank=True)

class Phone(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    target = models.ForeignKey(Target)

def get_file_path( instance, filename ):
    return "mail_files/%s/%s/%s" % ( instance.user, instance.category.id, filename )

class Mail(models.Model):
    category = models.ForeignKey(CategoryTarget, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    attach = models.FileField(null=True, blank=True, upload_to=get_file_path)
    attach2 = models.FileField(null=True, blank=True, upload_to=get_file_path)

    def save(self, force_insert=False, force_update=False, using=None):
        try:
            if not self.attach._committed:
                attach = Mail.objects.get(id=self.id).attach
                if attach:
                    os.remove(os.path.join(settings.MEDIA_ROOT, attach.name))
        except :
            pass
        try:
            if not self.attach2._committed:
                print self.attach2._committed
                print self.attach2.path
                attach2 = Mail.objects.get(id=self.id).attach2
                if attach2:
                    os.remove(os.path.join(settings.MEDIA_ROOT, attach2.name))
        except :
            pass
        super(Mail, self).save()

    def attachname(self):
        return os.path.basename(self.attach.name)

    def attachname2(self):
        return os.path.basename(self.attach2.name)
