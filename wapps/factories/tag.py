import factory

from taggit.models import Tag


class TagFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Tag {0}".format(n))
    # slug = factory.LazyAttribute(lambda n: slugify(n.name))

    class Meta:
        model = Tag
