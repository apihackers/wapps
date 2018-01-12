import factory

from wapps.models import Category


class CategoryFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Category {0}'.format(n))

    class Meta:
        model = Category
