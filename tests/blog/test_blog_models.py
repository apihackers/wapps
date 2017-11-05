import pytest

from wapps.blog.models import Blog, BlogPost

from wapps.pytest import assert_can_create_at, assert_can_not_create_at
from wapps.pytest import assert_allowed_subpage_types, assert_allowed_parent_types


@pytest.mark.django_db
def test_blog_hierarchy_restrictions(blog, site):
    assert_allowed_subpage_types(blog, [BlogPost])
    assert_can_create_at(site.root_page.__class__, Blog)
    assert_can_not_create_at(BlogPost, Blog)


@pytest.mark.django_db
def test_blogpost_hierarchy_restrictions(blog_post, site):
    assert_allowed_parent_types(blog_post, [Blog])
    assert_can_not_create_at(site.root_page.__class__, BlogPost)
    assert_can_create_at(Blog, BlogPost)
