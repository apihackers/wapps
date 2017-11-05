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
