import factory

from taggit.models import Tag


class TagFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Tag {0}".format(n))

    class Meta:
        model = Tag
