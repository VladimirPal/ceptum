          # -*- coding: utf-8 -*-
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os

def _add_thumb(s, completion):
    """ Изменяет строку(имя файла, URL), содержащую имя файла
    изображения, вставляя '.thumb' перед расширением имени файла
    (которое изменяется на '.png')
    """
    # split - возвращает список
    parts = s.split(".")
    parts.insert(-1, completion)
    if parts[-1].lower() not in 'png':
        parts[-1] = 'png'
    # join - объединяет список в строку
    return ".".join(parts)

class ThumbnailImageFieldFile(ImageFieldFile):
    def _get_thumb_path(self):
        return _add_thumb(self.path, self.field.completion)
    thumb_path = property(_get_thumb_path)

    def _get_thumb_url(self):
        return _add_thumb(self.url, self.field.completion)
    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)
        img.thumbnail(
            (self.field.thumb_width, self.field.thumb_height),
            Image.ANTIALIAS
        )
        img.save(self.thumb_path, 'PNG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width, thumb_height, completion, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        self.completion = completion
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
