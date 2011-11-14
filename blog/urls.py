from django.conf.urls.defaults import *
from blog.feeds import RssSiteNewsFeed

urlpatterns = patterns('',
                          url(r'^$', 'blog.views.blog', name="blog-page"),
                          url(r'^rss/$', RssSiteNewsFeed()),
                          url(r'^archive/(?P<when>[-\w]+)/$', 'blog.views.archive', name="archive-page"),
                          url(r'^category/(?P<category_slug>[-\w]+)/$', 'blog.views.category', name="categoryblog-page"),
                          url(r'^(?P<entry_slug>[-\w]+)/$', 'blog.views.entry', name="entry-page"),
)
