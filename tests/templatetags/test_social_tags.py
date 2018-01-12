import pytest

from wapps import social

pytestmark = pytest.mark.django_db


def test_social_url(jinja):
    assert jinja('{{ social_url("twitter", "apihackers") }}') == social.user_url('twitter', 'apihackers')


def test_social_icon(jinja):
    assert jinja('{{ social_icon("twitter") }}') == social.icon('twitter')


def test_social_share_url(jinja, faker):
    url = faker.url()
    title = faker.word()

    rendered = jinja('{{ social_share_url("twitter", url) }}', url=url)
    assert rendered == social.share_url('twitter', url)

    rendered = jinja('{{ social_share_url("twitter", url, title) }}', url=url, title=title)
    assert rendered == social.share_url('twitter', url, title)
