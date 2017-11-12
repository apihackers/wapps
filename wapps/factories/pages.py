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
    live = False

    class Meta:
        model = Page

    class Params:
        owned = factory.Trait(
            owner=factory.SubFactory(UserFactory),
        )
        root = factory.Trait(title='root', parent=None)

    @factory.lazy_attribute
    def parent(self):
        try:
            return Page.objects.get(slug='root')
        except Page.DoesNotExist:
            return PageFactory(root=True)

    @factory.post_generation
    def published(page, create, extracted, **kwargs):
        if not create:  # pragma: nocover
            # Simple build, do nothing.
            return

        if extracted is True:
            revision = page.save_revision()
            revision.publish()
            page.refresh_from_db()


class StaticPageFactory(PageFactory):
    body = factory.Faker('paragraph')
    seo_type = 'article'

    class Meta:
        model = StaticPage

    class Params:
        full = factory.Trait(
            intro=factory.Faker('paragraph'),
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
