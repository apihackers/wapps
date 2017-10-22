import pytest

from pytest_factoryboy import LazyFixture

from wapps import jsonld


@pytest.mark.django_db
def test_minimal(rf, site, identity):
    data = jsonld.graph({'request': rf.get('/')})

    assert data['@context'] == 'http://schema.org/'
    assert len(data['@graph']) == 2

    site_graph = data['@graph'][0]
    assert site_graph['@type'] == 'WebSite'
    assert site_graph['name'] == site.site_name
    assert site_graph['alternateName'] == identity.description
    assert site_graph['keywords'] == ','.join(t.name for t in identity.tags.all())
    assert site_graph['url'] == site.root_url

    org_graph = data['@graph'][1]
    assert org_graph['@type'] == 'Organization'
    assert org_graph['url'] == site.root_url
    assert org_graph['name'] == identity.name
