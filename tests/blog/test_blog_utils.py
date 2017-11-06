import pytest


from wapps.blog import utils


@pytest.mark.django_db
def test_get_site_blog(site, site_factory, blog_factory, faker):
    sites = site_factory.create_batch(3)
    blogs = [blog_factory(parent=site.root_page, published=True) for site in sites]

    for site, blog in zip(sites, blogs):
        assert utils.get_site_blog(site) == blog
