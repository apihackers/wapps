import factory

from wapps.models import IdentitySettings

from .image import ImageFactory
from .site import SiteFactory
from .tag import TagFactory


class IdentityFactory(factory.DjangoModelFactory):
    site = factory.SubFactory(SiteFactory)
    name = factory.Faker('word')
    description = factory.Faker('paragraph')
    logo = factory.SubFactory(ImageFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
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

    class Meta:
        model = IdentitySettings
        django_get_or_create = ['site']
