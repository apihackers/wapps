import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('blog__published', [True])
def test_minimal_blog_page(client, site, blog):
    response = client.get(blog.url)

    assert blog.get_parent() == site.root_page

    assert response.status_code == 200
