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
    ('3', u'До 4х недель'),
)

COLOR_CHOICES = (
    ('1', u'Черно-белая'),
    ('2', u'Цветная'),
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

    def __unicode__(self):
        return "%s, %s, %s, %s, %s, %s," % (self.type, self.get_camera_class_display(), self.get_location_display(), self.get_color_display(), self.resolution, self.price)

class Result(models.Model):
    camera = models.ManyToManyField(Camera)
    date = models.DateField(auto_now_add=True)
    installation = models.CharField(max_length=255, blank=True)
    arhive = models.CharField(choices=RECORDER_TIME_CHOICES, max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)

