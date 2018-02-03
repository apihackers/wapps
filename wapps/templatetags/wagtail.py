import jinja2

from django_jinja import library
from wagtail.wagtailcore.models import Page
from wagtail.contrib.wagtailroutablepage.templatetags.wagtailroutablepage_tags import (
    routablepageurl as dj_routablepageurl
)

from wapps.utils import get_image_url, get_site


@library.global_function
def menu():
    return Page.objects.live().in_menu().filter(depth__lte=3)


@library.global_function
@jinja2.contextfunction
def is_site_root(context, page):
    if 'request' not in context or not context['request'].site or not page:
        return False
    site = context['request'].site
    return site.root_page.pk == page.pk


@library.global_function
def imageurl(image, specs):
    return get_image_url(image, specs)


@library.global_function
@jinja2.contextfunction
def routablepageurl(context, page, name, *args, **kwargs):
    if not hasattr(context['request'], 'site'):  # pragma: nocover
        context['request'].site = get_site(context['request'])
    return dj_routablepageurl(context, page, name, *args, **kwargs)
