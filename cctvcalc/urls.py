from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'cctvcalc.views.calc', name="calc"),
    url(r'^result/(?P<result_id>[-\w]+)/$', 'cctvcalc.views.result', name="result-page"),
    url(r'^ajx-api$', 'cctvcalc.views.ajx_api', name="ajx-api"),
    url(r'^ajx-result$', 'cctvcalc.views.ajx_result', name="ajx-result"),
)