from django.conf.urls import url

from .feeds import BlogRssFeed, BlogAtomFeed

app_name = 'blog'

urlpatterns = [
    url(r'^feeds/rss/$', BlogRssFeed(), name="rss"),
    url(r'^feeds/atom/$', BlogAtomFeed(), name="atom"),
]
