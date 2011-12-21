          # -*- coding: utf-8 -*-
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('category-page', [str(self.slug)])

    class Meta:
        verbose_name_plural = 'Отрасли заказчиков'

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ManyToManyField(Category)
    date = models.DateField()
    entry = models.TextField()
    thumbnail_entry = models.TextField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/projects/%s/" % self.slug

    class Meta:
        ordering = ['date']

    class Meta:
        verbose_name_plural = 'Проекты'