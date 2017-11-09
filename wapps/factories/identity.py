import factory

from wapps.models import IdentitySettings

from .image import ImageFactory, SvgFileField
from .site import SiteFactory
from .tag import TagFactory


class IdentityFactory(factory.DjangoModelFactory):
    site = factory.SubFactory(SiteFactory)
    name = factory.Faker('word')
    description = factory.Faker('paragraph')

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


class FullIdentityFactory(IdentityFactory):
    logo = factory.SubFactory(ImageFactory)
    svg_logo = SvgFileField()
    favicon = factory.SubFactory(ImageFactory)
    amp_logo = factory.SubFactory(ImageFactory)
