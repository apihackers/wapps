import wapps


def test_python_metadata():
    assert hasattr(wapps, '__version__')
    assert hasattr(wapps, '__description__')


def test_django_app_config():
    assert wapps.default_app_config == 'wapps.apps.WappsConfig'
