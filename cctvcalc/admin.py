from django.contrib import admin
from cctvcalc.models import Camera

class CameraAdmin(admin.ModelAdmin):
    list_display = ('type', 'camera_class', 'location', 'color', 'resolution', 'price')

admin.site.register(Camera, CameraAdmin)
