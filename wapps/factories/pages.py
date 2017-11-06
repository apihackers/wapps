import factory

from wagtail_factories.factories import MP_NodeFactory
from wagtail.wagtailcore.models import Page
from wapps.models import StaticPage

from .image import ImageFactory
from .tag import TagFactory
from .user import UserFactory


class PageFactory(MP_NodeFactory):
    title = factory.Faker('sentence')
    seo_title = factory.Faker('sentence')
    search_description = factory.Faker('paragraph')

    class Meta:
        model = Page

    class Params:
        owned = factory.Trait(
            owner=factory.SubFactory(UserFactory),
        )

    @classmethod
    def _create(cls, *args, **kwargs):
        if 'parent' not in kwargs:
            try:
                kwargs['parent'] = Page.objects.get(depth=1)
            except Page.DoesNotExist:
                kwargs['parent'] = RootFactory()

        return super()._create(*args, **kwargs)

    @factory.post_generation
    def published(page, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted is True:
            revision = page.save_revision()
            revision.publish()
            page.refresh_from_db()

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


class RootFactory(PageFactory):
    depth = 1
    title = 'root'

    @classmethod
    def _create(cls, *args, **kwargs):
        kwargs['parent'] = None
        return super()._create(*args, **kwargs)


class StaticPageFactory(PageFactory):
    body = factory.Faker('paragraph')
    image = factory.SubFactory(ImageFactory)

    class Meta:
        model = StaticPage
