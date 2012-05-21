          # -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime

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
    callback = models.BooleanField(default=False)
    callback_at = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    done_at = models.DateField(null=True, blank=True)

class Phone(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    target = models.ForeignKey(Target)

