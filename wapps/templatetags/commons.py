import jinja2

from django.utils import timezone
from django.utils.safestring import mark_safe
from django_jinja import library

from .. import json, utils
from ..jsonld import graph


@library.filter(name='json')
def json_encode(data):
    return json.dumps(data)


@library.filter
@library.global_function
@jinja2.contextfunction
def jsonld(context, *data):
    if 'page' in context and hasattr(context['page'], '__jsonld__'):
        page = context['page']
        if page not in data:
            data = [page] + list(data)

    return mark_safe(''.join((
        '<script type="application/ld+json">',
        json.dumps(graph(context, *data)),
        '</script>'
    )))


@library.global_function
def now():
    return timezone.now()


@library.global_function
def timehash(length=10):
    return utils.timehash(length)


@library.global_function
@library.render_with('includes/pager.html')
@jinja2.contextfunction
def pager_for(page, previous_label=None, next_label=None):
    return {
        "page": page,
        'previous_label': previous_label,
        'next_label': next_label,
        # "querystring": querystring,
    }
