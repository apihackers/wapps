import os

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls
from wagtail.wagtailsearch.signal_handlers import register_signal_handlers as wagtailsearch_register_signal_handlers

from wapps import urls as wapps_urls

wagtailsearch_register_signal_handlers()


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^docs/', include(wagtaildocs_urls)),
    url(r'^search/', include(wagtailsearch_frontend_urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'', include(wapps_urls)),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += [
        url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'demo/images/favicon.ico'))
    ]
