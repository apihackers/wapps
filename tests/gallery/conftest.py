from pytest_factoryboy import register
from wapps.gallery import factories

register(factories.GalleryFactory)
register(factories.AlbumFactory)
register(factories.ManualAlbumFactory)
