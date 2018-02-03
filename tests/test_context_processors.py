import pytest


@pytest.mark.django_db
def test_google_api_key(jinja_context, settings, faker):
    settings.GOOGLE_API_KEY = faker.sentence()
    ctx = jinja_context()
    assert 'GOOGLE_API_KEY' in ctx
    assert ctx['GOOGLE_API_KEY'] == settings.GOOGLE_API_KEY


@pytest.mark.django_db
def test_google_analytics_id(jinja_context, settings, faker):
    settings.GOOGLE_ANALYTICS_ID = faker.sentence()
    ctx = jinja_context()
    assert 'GOOGLE_ANALYTICS_ID' in ctx
    assert ctx['GOOGLE_ANALYTICS_ID'] == settings.GOOGLE_ANALYTICS_ID


@pytest.mark.django_db
def test_wagtail_site_name(jinja_context, settings, faker):
    settings.WAGTAIL_SITE_NAME = faker.sentence()
    ctx = jinja_context()
    assert 'WAGTAIL_SITE_NAME' in ctx
    assert ctx['WAGTAIL_SITE_NAME'] == settings.WAGTAIL_SITE_NAME
