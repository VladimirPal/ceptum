from django.conf.urls.defaults import *

urlpatterns = patterns('',
                      url(r'^$', 'myadmin.views.auth', name="auth-page"),
                      url(r'^logout/$', 'myadmin.views.logout_view', name="logout-page"),
                      url(r'^clients/$', 'myadmin.views.clients', name="clients"),
                      url(r'^clients/add$', 'myadmin.views.add_client', name="add_client"),
                      url(r'^client/edit/(?P<id>[-\w]+)/$', 'myadmin.views.edit_client', name="edit-client"),)
