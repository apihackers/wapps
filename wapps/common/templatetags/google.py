from django.conf import settings

from django_jinja import library

from jinja2.ext import Extension


@library.extension
class GoogleSettings(Extension):
    def __init__(self, environment):
        super(GoogleSettings, self).__init__(environment)
        environment.globals['GOOGLE_API_KEY'] = getattr(settings, 'GOOGLE_API_KEY', None)
        environment.globals['GOOGLE_ANALYTICS_ID'] = getattr(settings, 'GOOGLE_ANALYTICS_ID', None)
