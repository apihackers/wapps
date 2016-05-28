from datetime import datetime

import jinja2

from django_jinja import library

from .. import json


@library.filter(name='json')
def json_encode(data):
    return json.dumps(data)


@library.global_function
def now():
    return datetime.now()


@library.global_function
@library.render_with('includes/pager.html')
@jinja2.contextfunction
def pager_for(page, previous_label=None, next_label=None):
    return {
        'previous_label': previous_label,
        'next_label': next_label,
        "page": page,
        # "querystring": querystring,
    }
