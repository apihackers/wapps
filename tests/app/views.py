from django.http import HttpResponse
from wapps.errors import HttpResponseError
from wapps.feed import SiteFeed
from wagtail.wagtailcore.models import Page


def error(request):
    response = HttpResponse('42', status=442)
    raise HttpResponseError(response)


def first_visit(request):
    return HttpResponse(request.session.get('first_visit'))


class TestFeed(SiteFeed):
    def items(self):
        qs = Page.objects.live()  # .descendant_of(self.site.root_page)
        return qs.order_by('-first_published_at')

    def item_link(self, item):
        return item.full_url


def site_feed(request, *args, **kwargs):
    feed = TestFeed()
    return feed(request, *args, **kwargs)
