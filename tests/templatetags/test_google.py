import pytest


@pytest.mark.django_db
def test_api_key(jinja_context, settings, faker):
    settings.GOOGLE_API_KEY = faker.sentence()
    ctx = jinja_context()
    assert 'GOOGLE_API_KEY' in ctx
    assert str(ctx['GOOGLE_API_KEY']) == str(settings.GOOGLE_API_KEY)


@pytest.mark.django_db
def test_analytics_id(jinja_context, settings, faker):
    settings.GOOGLE_ANALYTICS_ID = faker.sentence()
    ctx = jinja_context()
    assert 'GOOGLE_ANALYTICS_ID' in ctx
    assert str(ctx['GOOGLE_ANALYTICS_ID']) == str(settings.GOOGLE_ANALYTICS_ID)
