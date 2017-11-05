import pytest

from wapps import jsonld


@pytest.mark.django_db
def test_minimal(wrf, site, identity, blog):
    data = jsonld.graph({'request': wrf.get('/')}, blog)

    assert len(jsonld.extract(data['@graph'], 'Blog')) == 1

    graph = jsonld.extract_first(data['@graph'], 'Blog')
    assert graph['@id'] == blog.full_url
    assert graph['url'] == blog.full_url
    assert graph['name'] == blog.seo_title
    # assert graph['url'] == site.root_url
