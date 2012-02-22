          # -*- coding: utf-8 -*-
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('categoryblog-page', [str(self.slug)])

    class Meta:
        verbose_name_plural = 'Категории блога'

class Entry(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ManyToManyField(Category)
    date = models.DateField()
    entry = models.TextField()
    thumbnail_entry = models.TextField()
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    meta_keywords = models.CharField(max_length=300, blank=True, null=True)
    meta_description = models.CharField(max_length=300, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%s/" % self.slug

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Записи в блоге'
