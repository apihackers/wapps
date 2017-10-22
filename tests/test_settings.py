from django.conf import settings


def test_default_image_model():
    assert settings.WAGTAILIMAGES_IMAGE_MODEL == 'wapps.WappsImage'


def test_default_features():
    assert settings.WAPPS_FEATURES == ('word_count', )
