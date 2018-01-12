import factory
import pytest

from wapps.blog import utils


@pytest.mark.django_db
def test_get_site_blog(site_factory, blog_factory, page_factory, faker):
    sites = site_factory.create_batch(3,
                                      hostname=factory.Faker('domain_name'),
                                      root_page=factory.SubFactory(page_factory, root=True))
    blogs = [blog_factory(parent=site.root_page, published=True) for site in sites]

    for site, blog in zip(sites, blogs):
        assert utils.get_site_blog(site) == blog


@pytest.mark.django_db
def test_get_blog_from_context(wrf, site, blog_factory):
    blog = blog_factory(parent=site.root_page, published=True)

    ctx = {'request': wrf.get('/')}
    assert utils.get_blog_from_context(ctx) == blog
