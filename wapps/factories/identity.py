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

    class Meta:
        model = IdentitySettings
        django_get_or_create = ['site']


class FullIdentityFactory(IdentityFactory):
    tags = 3
    logo = factory.SubFactory(ImageFactory)
    svg_logo = SvgFileField()
    favicon = factory.SubFactory(ImageFactory)
    amp_logo = factory.SubFactory(ImageFactory)
    email = factory.Faker('email')
    telephone = factory.Faker('phone_number')
    address_1 = factory.Faker('street_address')
    post_code = factory.Faker('postalcode')
    city = factory.Faker('city')
    country = factory.Faker('country')
    facebook = factory.Faker('user_name')
    twitter = factory.Faker('user_name')
    linkedin = factory.Faker('uri')
    instagram = factory.Faker('user_name')
    pinterest = factory.Faker('user_name')
    youtube = factory.Faker('user_name')
