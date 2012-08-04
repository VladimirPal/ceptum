from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'cctvcalc.views.calc', name="calc"),
    url(r'^ajx-api$', 'cctvcalc.views.ajx_api', name="ajx-api"),
    url(r'^type-step1/$', 'cctvcalc.views.type', name="type"),
    url(r'^ip-step2/$', 'cctvcalc.views.ip', name="ip"),
    url(r'^ipcams-step3/$', 'cctvcalc.views.ipcams', name="ip-cams"),
    url(r'^recorder-step4/$', 'cctvcalc.views.recorder', name="rec"),
    url(r'^mic-step5/$', 'cctvcalc.views.mic', name="mic"),
    url(r'^install-step6/$', 'cctvcalc.views.install', name="install"),
    url(r'^result/$', 'cctvcalc.views.result', name="result"),
)