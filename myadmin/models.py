          # -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

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

class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_name = models.TextField()
    address = models.CharField(max_length=300, null=True)
    email = models.EmailField(max_length=100, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    status_date = models.DateField(null=True, blank=True)
    status_time = models.TimeField(null=True, blank=True)
    status_comment = models.CharField(max_length=500, blank=True)
    data = models.TextField(null=True)
    user = models.ForeignKey(User)
    referrer = models.CharField(max_length=50, choices=REFERRER_CHOICES)
    created_at = models.DateField(auto_now_add=True)

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
