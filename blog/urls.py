from django.conf.urls.defaults import *

urlpatterns = patterns('',
                          url(r'^$', 'blog.views.blog', name="blog-page"),
                          url(r'^archive/(?P<when>[-\w]+)/$', 'blog.views.archive', name="archive-page"),
                          url(r'^category/(?P<category_slug>[-\w]+)/$', 'blog.views.category', name="category-page"),
                          url(r'^(?P<entry_slug>[-\w]+)/$', 'blog.views.entry', name="entry-page"),
)
