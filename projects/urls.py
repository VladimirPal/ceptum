from django.conf.urls.defaults import *

urlpatterns = patterns('',
                          url(r'^$', 'projects.views.all_projects', name="projects-page"),
                          url(r'^category/(?P<category_slug>[-\w]+)/$', 'projects.views.category', name="category-page"),
                          url(r'^(?P<entry_slug>[-\w]+)/$', 'projects.views.project', name="project-page"),
)