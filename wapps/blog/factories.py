import factory

from wapps.factories import PageFactory, TagFactory, ImageFactory

from .models import Blog, BlogPost


class BlogFactory(PageFactory):

    class Meta:
        model = Blog


class BlogPostFactory(PageFactory):
    body = factory.Faker('sentence')

    class Meta:
        model = BlogPost


# class StaticPageFactory(PageFactory):
#     body = factory.Faker('paragraph')
#     image = factory.SubFactory(ImageFactory)
#
#     class Meta:
#         model = StaticPage
