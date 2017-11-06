import factory

from wagtail.wagtailcore.models import Site

from .pages import RootFactory


class SiteFactory(factory.DjangoModelFactory):
    hostname = 'localhost'
    port = factory.Sequence(lambda n: 8000 + n)
    site_name = 'Test Site'
    root_page = factory.SubFactory(RootFactory)
    is_default_site = True

    class Meta:
        model = Site
        django_get_or_create = ['hostname']
