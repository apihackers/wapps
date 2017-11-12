import pytest

from wapps import jsonld


@pytest.mark.django_db
def test_minimal(wrf, site, identity):
    data = jsonld.graph({'request': wrf.get('/')})

    assert data['@context'] == 'http://schema.org/'
    assert len(data['@graph']) == 2

    assert len(jsonld.extract(data['@graph'], 'WebSite')) == 1
    site_graph = jsonld.extract_first(data['@graph'], 'WebSite')
    assert site_graph['name'] == site.site_name
    assert site_graph['alternateName'] == identity.description
    assert site_graph['keywords'] == ','.join(t.name for t in identity.tags.all())
    assert site_graph['url'] == site.root_url

    assert len(jsonld.extract(data['@graph'], 'Organization')) == 1
    org_graph = jsonld.extract_first(data['@graph'], 'Organization')
    assert org_graph['url'] == site.root_url
    assert org_graph['name'] == identity.name


@pytest.mark.django_db
def test_minimal_static_page(wrf, site, identity, static_page):
    data = jsonld.graph({'request': wrf.get('/')}, static_page)

    assert len(jsonld.extract(data['@graph'], 'Article')) == 1
    graph = jsonld.extract_first(data['@graph'], 'Article')

    assert graph['@id'] == static_page.full_url
    assert graph['url'] == static_page.full_url
    assert graph['name'] == static_page.seo_title
    assert 'keywords' not in graph


@pytest.mark.django_db
def test_full_static_page(wrf, site, identity, static_page_factory):
    page = static_page_factory(published=True, owned=True, full=True, tags=3)
    data = jsonld.graph({'request': wrf.get('/')}, page)

    assert len(jsonld.extract(data['@graph'], 'Article')) == 1
    graph = jsonld.extract_first(data['@graph'], 'Article')

    assert graph['keywords'] == ','.join(t.name for t in page.tags.all())


@pytest.mark.django_db
@pytest.mark.parametrize('static_page__seo_type', ['service'])
def test_service_static_page(wrf, site, identity, static_page):
    data = jsonld.graph({'request': wrf.get('/')}, static_page)

    assert len(jsonld.extract(data['@graph'], 'Service')) == 1
    graph = jsonld.extract_first(data['@graph'], 'Service')

    assert graph['@id'] == static_page.full_url
    assert graph['url'] == static_page.full_url
    assert graph['name'] == static_page.seo_title


@pytest.mark.django_db
@pytest.mark.parametrize('static_page__seo_type', ['faq'])
def test_faq_static_page(wrf, site, identity, static_page):
    data = jsonld.graph({'request': wrf.get('/')}, static_page)

    assert len(jsonld.extract(data['@graph'], 'FAQPage')) == 1
    graph = jsonld.extract_first(data['@graph'], 'FAQPage')

    assert graph['@id'] == static_page.full_url
    assert graph['url'] == static_page.full_url
    assert graph['name'] == static_page.seo_title
