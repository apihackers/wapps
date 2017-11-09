import pytest

from wapps import jsonld


@pytest.mark.django_db
def test_minimal_gallery(wrf, site, identity, gallery):
    data = jsonld.graph({'request': wrf.get('/')}, gallery)

    assert len(jsonld.extract(data['@graph'], 'CollectionPage')) == 1
    graph = jsonld.extract_first(data['@graph'], 'CollectionPage')

    assert graph['@id'] == gallery.full_url
    assert graph['url'] == gallery.full_url
    assert graph['name'] == gallery.seo_title


@pytest.mark.django_db
def test_minimal_album(wrf, site, identity, album):
    data = jsonld.graph({'request': wrf.get('/')}, album)

    assert len(jsonld.extract(data['@graph'], 'ImageGallery')) == 1
    graph = jsonld.extract_first(data['@graph'], 'ImageGallery')

    assert graph['@id'] == album.full_url
    assert graph['name'] == album.seo_title


@pytest.mark.django_db
def test_full_gallery_with_albums(wrf, site, identity, gallery_factory, album_factory):
    gallery = gallery_factory(full=True)
    albums = album_factory.create_batch(3, full=True, live=True, parent=gallery)
    data = jsonld.graph({'request': wrf.get('/')}, gallery)

    assert len(jsonld.extract(data['@graph'], 'CollectionPage')) == 1
    graph = jsonld.extract_first(data['@graph'], 'CollectionPage')

    assert graph['@id'] == gallery.full_url
    assert graph['url'] == gallery.full_url
    assert graph['name'] == gallery.seo_title

    assert 'hasPart' in graph
    assert len(graph['hasPart']) == len(albums)
    for part in graph['hasPart']:
        assert part['@type'] == 'ImageGallery'
