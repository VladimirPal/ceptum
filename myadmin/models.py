          # -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('CALL', 'Созвон'),
    ('OFFER', 'Скинуть КП'),
    ('INSPECTION', 'Осмотр'),
    ('PROJECT', 'Проект'),
 )

class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=100, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    status_time = models.DateTimeField(null=True,blank=True)
    status_comment = models.CharField(max_length=500, blank=True)
    data = models.TextField(null=True)
    user = models.ForeignKey(User)
    file = models.ManyToManyField('ClientFile', null=True)
    comment = models.ManyToManyField('Comment', null=True)

class ClientFile(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='./clientfiles')

class Comment(models.Model):
    user = models.ManyToManyField(User)
    comment = models.TextField()
    file = models.ManyToManyField(ClientFile)
