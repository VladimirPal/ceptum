# -*- coding: utf-8 -*-
from django.db import models


TYPE_CHOICES = (
    ('IP', u'IP система'),
    ('ANALOG', u'Аналоговая система'),
)

CLASS_CHOICES = (
    ('BEGIN', u'Бюджетная система'),
    ('MIDDLE', u'Система среднего уровня'),
    ('PRO', u'Система профессионального уровня'),
)

RECORDER_TIME_CHOICES = (
    ('1', u'До 2х недель'),
    ('2', u'2-4 недели'),
    ('3', u'От 4х недель'),
)

COLOR_CHOICES = (
    ('0', u'Черно-белая'),
    ('1', u'Цветная'),
)

LOCATION_CHOICES = (
    ('1', u'Внутренняя'),
    ('2', u'Уличная'),
)

class Camera(models.Model):
    type = models.CharField(choices=TYPE_CHOICES, max_length=100)
    camera_class = models.CharField(choices=CLASS_CHOICES, max_length=100)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=100)
    color = models.CharField(choices=COLOR_CHOICES, max_length=100)
    resolution = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)
