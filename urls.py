# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

from django.contrib import admin
admin.autodiscover()
handler500 = 'cctvision.catalog.views.internal_error'

urlpatterns = patterns('',
    (r'^', include('cctvision.catalog.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^cart/', include('cctvision.cart.urls')),
    (r'^blog/', include('cctvision.blog.urls')),
    (r'^myadmin/', include('cctvision.myadmin.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^grappelli/', include('grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns ('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()