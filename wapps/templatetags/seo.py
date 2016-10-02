import jinja2

from django_jinja import library

from ..metadata import Metadata


@library.global_function
@jinja2.contextfunction
def page_meta(context, **kwargs):
    return Metadata(context, **kwargs)
