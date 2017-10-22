from django.test import RequestFactory as BaseRequestFactory

from .site import SiteFactory


class RequestFactory(BaseRequestFactory):
    def __init__(self, site=None, user=None, **defaults):
        super().__init__(**defaults)
        self.site = site
        self.user = user

    def request(self, user=None, site=None, **kwargs):
        request = super(RequestFactory, self).request(**kwargs)
        request.site = site or self.site or SiteFactory()
        request.user = user or self.user
        return request
