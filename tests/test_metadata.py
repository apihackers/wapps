import pytest

from wapps.metadata import Metadata
from wapps.utils import get_image_url

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('identity__tags', [3])
def test_from_kwargs(rf, page, site, identity):
    metadata = Metadata(request=rf.get('/'), page=page, site=site)

    assert metadata.title == page.seo_title
    assert metadata.site_title == identity.name
    assert metadata.full_title == ' | '.join((page.seo_title, identity.name))
    assert metadata.description == page.search_description
    assert metadata.image == identity.logo
    assert metadata.image_url == site.root_url + get_image_url(identity.logo, 'original')
    assert len(metadata.tags) == 3


def test_from_context(rf, page, site, identity):
    ctx = {'request': rf.get('/'), 'page': page, 'site': site}
    metadata = Metadata(ctx)

    assert metadata.title == page.seo_title
    assert metadata.site_title == identity.name
    assert metadata.full_title == ' | '.join((page.seo_title, identity.name))
    assert metadata.description == page.search_description


def test_title_from_kwargs(rf, page, site, faker):
    title = faker.sentence()
    metadata = Metadata(request=rf.get('/'), page=page, site=site, title=title)

    assert metadata.title == title


def test_description_from_kwargs(rf, page, site, faker):
    description = faker.paragraph()
    metadata = Metadata(request=rf.get('/'), page=page, site=site, description=description)

    assert metadata.description == description


@pytest.mark.parametrize('identity__name', [None])
def test_no_identity_name(rf, page, site, identity):
    metadata = Metadata(request=rf.get('/'), page=page, site=site)

    assert metadata.full_title == page.seo_title


@pytest.mark.parametrize('page__seo_title', [''])
def test_no_seo_title(rf, page, site, identity):
    metadata = Metadata(request=rf.get('/'), page=page, site=site)

    assert metadata.title == page.title


@pytest.mark.parametrize('page__search_description', [''])
def test_no_search_description(rf, page, site, identity):
    metadata = Metadata(request=rf.get('/'), page=page, site=site)

    assert metadata.description == identity.description


def test_no_page(rf, site, identity):
    metadata = Metadata(request=rf.get('/'), site=site)

    assert metadata.title is None
    assert metadata.site_title == identity.name
    assert metadata.full_title == identity.name
    assert metadata.description == identity.description


@pytest.mark.parametrize('static_page__tags', [['static-1', 'static-2']])
@pytest.mark.parametrize('identity__tags', [['identity-1', 'identity-2']])
def test_tags(rf, static_page, site, identity):
    metadata = Metadata(request=rf.get('/'), page=static_page, site=site, tags=['tag-1', 'tag-2'])

    assert metadata.tags == {'tag-1', 'tag-2', 'static-1', 'static-2', 'identity-1', 'identity-2'}


def test_page_image(rf, static_page, site, identity):
    metadata = Metadata(request=rf.get('/'), page=static_page, site=site)

    assert metadata.image == static_page.image


def test_image_from_kwargs(rf, page, site, image):
    metadata = Metadata(request=rf.get('/'), page=page, site=site, image=image)

    assert metadata.image == image


def test_image_url_from_kwargs(rf, page, site, faker):
    url = faker.url()
    metadata = Metadata(request=rf.get('/'), page=page, site=site, image_url=url)

    assert metadata.image_url == url


@pytest.mark.parametrize('identity__logo', [None])
def test_no_image(rf, page, site, identity):
    metadata = Metadata(request=rf.get('/'), page=page, site=site)

    assert metadata.image is None
    assert metadata.image_url is None
