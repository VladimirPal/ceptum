          # -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

CAUSE_CHOICES = (
    ('FROM_CLIENT', 'С продажи'),
    ('SALARY_VLADIMIR', 'Зарплата Владимиру'),
    ('SALARY_VICTOR', 'Зарплата Виктору'),
    ('SALARY_COURIER', 'Зарплата курьеру'),
    ('PURCHASE', 'Закупка товара'),
    ('BRIBE', 'Взятка'),
    ('SENDGOODS', 'Отправка товара'),
    ('PHONE', 'На телефон'),
    ('Yandex', 'Яндекс Директ'),
    ('OTHER', 'Прочее'),
)

TYPE_CHOICES = (
    ('ENCASH', 'Наличные'),
    ('WEBMONEY', 'Webmoney'),
    ('YANDEX', 'Яндекс'),
)

class Cash(models.Model):
    date = models.DateField(auto_now_add=True)
    cashflow = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Поток")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    cause = models.CharField(max_length=200 ,choices=CAUSE_CHOICES, verbose_name="Причина")
    type = models.CharField(default='Encash',max_length=200 ,choices=TYPE_CHOICES, verbose_name="Тип")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="Комментарий")

    class Meta:
        ordering = ['-id']

class Balance(models.Model):
    yandex = models.DecimalField(max_digits=10, decimal_places=2)
    webmoney = models.DecimalField(max_digits=10, decimal_places=2)
    encash = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Waytmoney(models.Model):
    wayt_money = models.DecimalField(max_digits=20, decimal_places=2)

class Cash_statistic(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=200 ,choices=TYPE_CHOICES, verbose_name="Тип")
    cash = models.DecimalField(max_digits=10, decimal_places=2)

class Product_statistic(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    cash = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.product

class Task(models.Model):
    title = models.CharField(max_length=500, verbose_name="Название")
    task = models.TextField()
    is_done = models.BooleanField(verbose_name="Готово?")
    user = models.CharField(max_length=200)
    performers = models.ManyToManyField(User)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

class TaskAnswer(models.Model):
    task = models.ForeignKey(Task)
    answer = models.TextField()
    user = models.CharField(max_length=200)
    file = models.FileField(upload_to='./taskfiles')
    date = models.DateTimeField(auto_now_add=True)

class TaskFile(models.Model):
    task = models.ForeignKey(Task)
    file = models.FileField(upload_to='./taskfiles')

    def __unicode__(self):
        return str(self.file).split('/')[1]

class Order(models.Model):
    title = models.CharField(max_length=300, verbose_name="Название")
    order = models.TextField()
    tracking_number = models.CharField(max_length=200)
    invoice = models.FileField(upload_to="./invoices")
    is_done = models.BooleanField(verbose_name="Доставлено?")
    user = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
