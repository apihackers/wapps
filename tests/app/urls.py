from django.conf.urls import include, url
# from django.conf import settings
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from wapps import urls as wapps_common_urls

from .views import error, first_visit


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/', include('wagtail.wagtailsearch.urls.frontend')),

    # Test views
    url(r'^error/$', error, name='error'),
    url(r'^first-visit/$', first_visit, name='first-visit'),

    # url(r'^i18n/', include('django.conf.urls.i18n')),

    # url(r'^forms/', include(wapps_forms_urls)),
    # url('^sitemap\.xml$', sitemap),

    # url(r'^feeds/blog/rss/$', BlogRssFeed(), name="blog_rss_feed"),
    # url(r'^feeds/blog/atom/$', BlogAtomFeed(), name="blog_atom_feed"),

    url(r'', include(wapps_common_urls)),
    url(r'', include(wagtail_urls)),
]
