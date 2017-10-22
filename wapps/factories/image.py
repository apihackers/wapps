import factory

from wagtail.wagtailimages.tests.utils import get_image_model, get_test_image_file


class ImageFactory(factory.DjangoModelFactory):
    title = factory.Faker('word')
    file = get_test_image_file()

    class Meta:
        model = get_image_model()
