from __future__ import absolute_import

from django.conf.urls import url
from wagtail.wagtailimages.views.serve import ServeView

from .api import router
from .views import image

urlpatterns = [
    url(r'^api/v1/', router.urls),
    url('^images/(?P<pk>\d+)/(?P<specs>.+)$', image, name='image'),
    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),
]
