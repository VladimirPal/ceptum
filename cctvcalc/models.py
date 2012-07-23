# -*- coding: utf-8 -*-
from django.db import models

SYSTEM_TYPE_CHOICES = (
    ('BEGIN', u'Система начального уровня'),
    ('MIDDLE', u'Система среднего уровня'),
    ('PRO', u'Система профессионального уровня'),
    )

ANALOG_CAMS_CHOICES = (
    ('LOW', u'Низкого разрешения(420 ТВЛ)'),
    ('STANDART', u'Стандартного разрешения(540 - 600 ТВЛ)'),
    ('HIGH', u'Высокого разрешения(700 ТВЛ)'),
    )

IP_CAMS_CHOICES = (
    ('1', u'640x480'),
    ('2', u'702x576'),
    ('3', u'1280x1024'),
    )

RECORDER_TIME_CHOICES = (
    ('1', u'До 2х недель'),
    ('2', u'2-4 недели'),
    ('3', u'От 4х недель'),
    )

SPEED_RECORD_CHOICES = (
    ('1', u'1-12,5 кадров в секунду'),
    ('2', u'12.5-25 кадров в секунду'),
    )

COLOR_CHOICES = (
    ('0', u'Черно-белая'),
    ('1', u'Цветная'),
    )

STREET_CHOICES = (
    ('0', u'Внутренняя'),
    ('1', u'Уличная'),
)

class CalcCart(models.Model):
    calc_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    system_type = models.CharField(choices=SYSTEM_TYPE_CHOICES, max_length=200)
    is_ip = models.BooleanField(blank=True)
    recorder_time = models.CharField(choices=RECORDER_TIME_CHOICES, max_length=200, blank=True)
    speed_record = models.CharField(choices=SPEED_RECORD_CHOICES, max_length=200, blank=True)
    count_microfone = models.IntegerField(null=True, blank=True)
    cable_length = models.CharField(blank=True, max_length=200)

class IpCams(models.Model):
    cart = models.ForeignKey(CalcCart)
    resolution = models.CharField(choices=IP_CAMS_CHOICES, max_length=200)
    is_street = models.CharField(choices=STREET_CHOICES, max_length=200)
    count = models.IntegerField()

class AnalogCams(models.Model):
    cart = models.ForeignKey(CalcCart)
    resolution = models.CharField(choices=ANALOG_CAMS_CHOICES, max_length=200)
    is_color = models.CharField(choices=COLOR_CHOICES, max_length=200, blank=True)
    is_street = models.CharField(choices=STREET_CHOICES, max_length=200, blank=True)
    count = models.IntegerField()
