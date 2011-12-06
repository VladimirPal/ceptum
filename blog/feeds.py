from django.contrib.syndication.views import Feed
from blog.models import Entry

class RssSiteNewsFeed(Feed):
    title = "Ceptum Blog"
    link = "ceptum.ru/blog/rss/"

    def items(self):
        return Entry.objects.order_by('-date')[:5]

    def item_description(self, item):
        return item.entry
