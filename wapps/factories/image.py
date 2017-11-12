import factory
import pkg_resources
import random

from django.core import files

from wagtail.wagtailimages.tests.utils import get_image_model, get_test_image_file

from .tag import TagFactory

SVG_FILES = ['wagtail.svg', 'django-logo-negative.svg', 'django-logo-positive.svg']


class ImageFactory(factory.DjangoModelFactory):
    title = factory.Faker('word')
    file = get_test_image_file()

    class Meta:
        model = get_image_model()

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


class SvgFileField(factory.django.FileField):
    def generate(self, sequence, obj, create, params):
        params = super(SvgFileField, self).generate(sequence, obj, create, params)
        filename = random.choice(SVG_FILES)
        f = pkg_resources.resource_stream(__name__, filename)
        return files.File(f, filename)
