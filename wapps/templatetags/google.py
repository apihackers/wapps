from django_jinja import library

from jinja2.ext import Extension

from wapps.utils import SettingProxy


@library.extension
class GoogleSettings(Extension):
    def __init__(self, environment):
        super(GoogleSettings, self).__init__(environment)
        environment.globals['GOOGLE_API_KEY'] = SettingProxy('GOOGLE_API_KEY')
        environment.globals['GOOGLE_ANALYTICS_ID'] = SettingProxy('GOOGLE_ANALYTICS_ID')
