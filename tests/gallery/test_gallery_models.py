import pytest

from pytest_factoryboy import LazyFixture

from wapps.gallery.models import Gallery


@pytest.mark.django_db
@pytest.mark.parametrize('album__parent', [LazyFixture('gallery')])
def test_album_parent_gallery(gallery, album):
    assert isinstance(album.gallery, Gallery)
    assert album.gallery == gallery


@pytest.mark.django_db
def test_root_album_has_no_parent_gallery(album):
    assert album.gallery is None
