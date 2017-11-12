import factory
from factory.fuzzy import FuzzyChoice

from wapps.factories import PageFactory, TagFactory, ImageFactory

from .models import Gallery, Album, ManualAlbum, ManualAlbumImage


class GalleryFactory(PageFactory):

    class Meta:
        model = Gallery

    class Params:
        full = factory.Trait(
            intro=factory.Faker('paragraph'),
            feed_image=factory.SubFactory(ImageFactory),
        )


class AlbumFactory(PageFactory):
    animation = FuzzyChoice(a[0] for a in Album.ANIMATIONS_TYPES)

    class Meta:
        model = Album

    class Params:
        full = factory.Trait(
            intro=factory.Faker('sentence'),
            image=factory.SubFactory(ImageFactory),
        )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:  # pragma: nocover
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them.
            if isinstance(extracted, int):
                tags = TagFactory.create_batch(extracted)
            else:
                tags = extracted
            for tag in tags:
                self.tags.add(tag)


class ManualAlbumFactory(AlbumFactory):
    class Meta:
        model = ManualAlbum

    @factory.post_generation
    def images(self, create, extracted, **kwargs):
        if not create:  # pragma: nocover
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them.
            if isinstance(extracted, int):
                images = [ManualAlbumImage(image=i) for i in ImageFactory.create_batch(extracted)]
            else:
                images = extracted
            for image in images:
                self.images.add(image)
