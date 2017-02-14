import jinja2

from django.conf import settings
from django_jinja import library
from jinja2.ext import Extension
from wagtail.wagtailcore.models import Page
from wagtail.contrib.wagtailroutablepage.templatetags.wagtailroutablepage_tags import (
    routablepageurl as dj_routablepageurl
)

from wapps.utils import get_image_url


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
    return dj_routablepageurl(context, page, name, *args, **kwargs)


@library.extension
class WagtailSettings(Extension):
    def __init__(self, environment):
        super(WagtailSettings, self).__init__(environment)
        environment.globals['WAGTAIL_SITE_NAME'] = getattr(settings, 'WAGTAIL_SITE_NAME', None)
