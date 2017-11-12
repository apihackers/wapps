import pytest

from pytest_factoryboy import LazyFixture

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures('site'),
]


@pytest.mark.parametrize('gallery__published', [True])
def test_minimal_gallery_page(client, gallery):
    response = client.get(gallery.url)

    assert response.status_code == 200
    assert response.context_data['page'] == gallery


@pytest.mark.parametrize('gallery__published', [True])
def test_gallery_with_albums(client, gallery, album_factory, manual_album_factory):
    albums = album_factory.create_batch(3, published=True, parent=gallery)
    manual_albums = manual_album_factory.create_batch(3, published=True, parent=gallery, images=3)

    response = client.get(gallery.url)

    assert response.status_code == 200

    ctx = response.context_data

    assert ctx['page'] == gallery
    assert len(ctx['albums']) == len(albums) + len(manual_albums)


@pytest.mark.parametrize('album__published', [True])
@pytest.mark.parametrize('album__parent', [LazyFixture('gallery')])
def test_minimal_album_page(client, album):
    response = client.get(album.url)

    assert response.status_code == 200
    assert response.context_data['page'] == album


def test_full_album_page(client, tag, album_factory, image_factory):
    images = image_factory.create_batch(3, tags=[tag])
    album = album_factory(full=True, published=True, tags=[tag])
    response = client.get(album.url)

    assert response.status_code == 200
    assert response.context_data['page'] == album
    assert len(response.context_data['images']) == len(images)


@pytest.mark.parametrize('manual_album__published', [True])
@pytest.mark.parametrize('manual_album__parent', [LazyFixture('gallery')])
def test_minimal_manual_album_page(client, manual_album):
    response = client.get(manual_album.url)

    assert response.status_code == 200
    assert response.context_data['page'] == manual_album


def test_full_manual_album_page(client, tag, manual_album_factory):
    album = manual_album_factory(full=True, published=True, images=3)
    response = client.get(album.url)

    assert response.status_code == 200
    assert response.context_data['page'] == album
    assert len(response.context_data['images']) == 3
