import factory

from wagtail.wagtailcore.models import Site, Page

from .pages import PageFactory


class SiteFactory(factory.DjangoModelFactory):
    hostname = 'localhost'
    port = factory.Sequence(lambda n: 8000 + n)
    site_name = 'Test Site'
    is_default_site = True

    @factory.lazy_attribute
    def root_page(self):
        try:
            return Page.objects.get(slug='root')
        except Page.DoesNotExist:
            return PageFactory(root=True)

    class Meta:
        model = Site
        django_get_or_create = ['hostname']
