from __future__ import absolute_import

from django.conf import settings
from django.conf.urls import url
from wagtail.wagtailimages.views.serve import ServeView

from .api import router
from .views import image

urlpatterns = [
    url(r'^api/v1/', router.urls),
    url('^images/(?P<pk>\d+)/(?P<specs>.+)$', image, name='image'),
    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),
]

if settings.DEBUG:
    from django.views.generic import TemplateView

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    ]
