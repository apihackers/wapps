import factory
import pkg_resources
import random

from django.core import files

from wagtail.wagtailimages.tests.utils import get_image_model, get_test_image_file

SVG_FILES = ['wagtail.svg', 'django-logo-negative.svg', 'django-logo-positive.svg']


class ImageFactory(factory.DjangoModelFactory):
    title = factory.Faker('word')
    file = get_test_image_file()

    class Meta:
        model = get_image_model()


class SvgFileField(factory.django.FileField):
    def generate(self, sequence, obj, create, params):
        params = super(SvgFileField, self).generate(sequence, obj, create, params)
        filename = random.choice(SVG_FILES)
        f = pkg_resources.resource_stream(__name__, filename)
        return files.File(f, filename)
