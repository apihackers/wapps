from urllib import parse

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from wagtail.wagtailcore.models import Site


class BlogRssFeed(Feed):
    def __call__(self, request, *args, **kwargs):
        from .models import Blog
        self.request = request
        self.blog = kwargs.get('blog') or Blog.objects.first()
        return super(BlogRssFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return self.blog.title

    def description(self):
        return self.blog.intro

    def link(self):
        return self.blog.slug

    def items(self):
        return self.blog.get_queryset()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_pubdate(self, item):
        return item.date

    def item_link(self, item):
        return item.full_url

    def item_enclosure_url(self, item):
        if item.image:
            site = Site.find_for_request(self.request)
            return parse.urljoin(site.root_url, item.image.file.url)
        return None


class BlogAtomFeed(BlogRssFeed):
    feed_type = Atom1Feed
    subtitle = BlogRssFeed.description
