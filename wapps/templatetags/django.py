from django.utils import formats

from django_jinja import library

from jinja2.ext import Extension


# @library.global_function
# def media(url):
#     return ''.join([settings.MEDIA_URL, url]) if url else None


@library.extension
class DjangoCompat(Extension):
    def __init__(self, environment):
        super(DjangoCompat, self).__init__(environment)
        environment.filters['localize'] = formats.localize
