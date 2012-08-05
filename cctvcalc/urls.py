from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'cctvcalc.views.calc', name="calc"),
    url(r'^ajx-api$', 'cctvcalc.views.ajx_api', name="ajx-api"),
)