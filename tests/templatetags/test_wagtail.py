import pytest

from wapps.utils import get_image_url


@pytest.mark.django_db
def test_wagtail_site_name(jinja, settings, faker):
    settings.WAGTAIL_SITE_NAME = faker.sentence()
    rendered = jinja('{{ WAGTAIL_SITE_NAME }}')
    assert rendered == settings.WAGTAIL_SITE_NAME


@pytest.mark.django_db
def test_is_site_root(rf, jinja, site, page):
    request = rf.get('/')
    assert jinja('{{ is_site_root(page) }}', request=request, page=site.root_page) == 'True'
    assert jinja('{{ is_site_root(page) }}', request=request, page=page) == 'False'
    assert jinja('{{ is_site_root(page) }}', page=site.root_page) == 'False'
    assert jinja('{{ is_site_root(page) }}', request=request, page=None) == 'False'


@pytest.mark.django_db
def test_imageurl(image, jinja):
    rendered = jinja('{{ imageurl(image, "original") }}', image=image)
    assert rendered == get_image_url(image, 'original')
