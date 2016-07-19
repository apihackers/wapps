from datetime import datetime

import jinja2

from django.utils.safestring import mark_safe
from django_jinja import library

from .. import json


@library.filter(name='json')
def json_encode(data):
    return json.dumps(data)


@library.filter
@library.global_function
@jinja2.contextfunction
def jsonld(context, data):
    if data and hasattr(data, '__jsonld__'):
        data_jsonld = data.__jsonld__(context)
        if not data_jsonld:
            return ''
        elif isinstance(data_jsonld, dict):
            jsonld = data_jsonld
            if '@context' not in jsonld:
                jsonld['@context'] = 'http://schema.org/'
        else:
            jsonld = {
                "@context": 'http://schema.org/',
                "@graph": data_jsonld
            }
        return mark_safe(''.join((
            '<script type="application/ld+json">',
            json.dumps(jsonld),
            '</script>'
        )))
    else:
        return ''


@library.global_function
def now():
    return datetime.now()


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
