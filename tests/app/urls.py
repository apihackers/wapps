from django.conf.urls import include, url
# from django.conf import settings
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
# from wagtail.contrib.wagtailsitemaps.views import sitemap

from wapps import urls as wapps_common_urls
from wapps.forms import urls as wapps_forms_urls

# from ..feeds import BlogRssFeed, BlogAtomFeed


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/', include('wagtail.wagtailsearch.urls.frontend')),
    # url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^forms/', include(wapps_forms_urls)),
    # url('^sitemap\.xml$', sitemap),

    # url(r'^feeds/blog/rss/$', BlogRssFeed(), name="blog_rss_feed"),
    # url(r'^feeds/blog/atom/$', BlogAtomFeed(), name="blog_atom_feed"),

    url(r'', include(wapps_common_urls)),
    url(r'', include(wagtail_urls)),
]


# if settings.DEBUG:
#     from django.conf.urls.static import static
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#     # Serve static and media files from development server
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
#     if getattr(settings, 'DEBUG_TOOLBAR', False):
#         import debug_toolbar
#         urlpatterns.insert(0, url(r'^__debug__/', include(debug_toolbar.urls)))
