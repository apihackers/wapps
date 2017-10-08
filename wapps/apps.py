from django.apps import AppConfig
from appconf import AppConf


class WappsConfig(AppConfig):
    name = 'wapps'
    label = 'wapps'
    verbose_name = 'Wagtail Apps'


class WappsSettings(AppConf):
    '''Wapps default settings'''
    FEATURES = (
        'word_count',
    )

    class Meta:
        prefix = 'wapps'


class WagtailSettings(AppConf):
    '''Wagtail default settings'''
    WAGTAILIMAGES_IMAGE_MODEL = 'wapps.WappsImage'
