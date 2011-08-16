from django.db import models
from tinymce import models as tinymce_models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('category-page', [str(self.slug)])

class Entry(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ManyToManyField(Category)
    date = models.DateTimeField()
    entry = tinymce_models.HTMLField()
    thumbnail_entry = tinymce_models.HTMLField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%s/" % self.slug

    class Meta:
        ordering = ['-date']
