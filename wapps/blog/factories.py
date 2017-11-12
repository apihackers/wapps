import factory

from wapps.factories import PageFactory, TagFactory, ImageFactory, CategoryFactory

from .models import Blog, BlogPost, BlogPostCategory


class BlogFactory(PageFactory):

    class Meta:
        model = Blog

    class Params:
        full = factory.Trait(
            intro=factory.Faker('paragraph'),
            image=factory.SubFactory(ImageFactory),
        )


class BlogPostFactory(PageFactory):
    body = factory.Faker('paragraph')

    class Meta:
        model = BlogPost

    class Params:
        full = factory.Trait(
            excerpt=factory.Faker('sentence'),
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

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:  # pragma: nocover
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them.
            if isinstance(extracted, int):
                categories = CategoryFactory.create_batch(extracted)
            else:
                categories = extracted
            for category in categories:
                self.blogpost_categories.add(BlogPostCategory(category=category))
