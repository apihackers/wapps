from __future__ import absolute_import

from django.conf.urls import url

from .api import router
from .views import image

urlpatterns = [
    url(r'^api/v1/', router.urls),
    url('^images/(?P<pk>\d+)/(?P<specs>.+)$', image, name='image'),
]
