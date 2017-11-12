import pytest

from pytest_factoryboy import LazyFixture

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures('site'),
]


@pytest.mark.parametrize('blog__published', [True])
def test_minimal_blog_page(client, blog):
    response = client.get(blog.url)

    assert response.status_code == 200
    assert response.context_data['page'] == blog


@pytest.mark.parametrize('blog__published', [True])
def test_blog_with_posts(client, blog, blog_post_factory):
    posts = blog_post_factory.create_batch(3, published=True, parent=blog)

    response = client.get(blog.url)

    assert response.status_code == 200

    ctx = response.context_data

    assert ctx['page'] == blog
    assert len(ctx['posts']) == len(posts)


@pytest.mark.parametrize('blog__published', [True])
def test_blog_with_posts_by_category(client, blog, category, blog_post_factory):
    posts = blog_post_factory.create_batch(3, published=True, parent=blog, categories=[category])
    excluded_posts = blog_post_factory.create_batch(2, published=True, parent=blog, categories=2)

    url = blog.url + blog.reverse_subpage('by_category', kwargs={'category': category.slug})
    response = client.get(url)

    assert response.status_code == 200

    ctx = response.context_data

    assert ctx['page'] == blog
    assert len(ctx['posts']) == len(posts)

    for post in posts:
        assert post in ctx['posts']

    for post in excluded_posts:
        assert post not in ctx['posts']


@pytest.mark.parametrize('blog__published', [True])
def test_blog_with_posts_by_tag(client, blog, blog_post_factory):
    posts = blog_post_factory.create_batch(3, published=True, parent=blog, tags=['test'])
    excluded_posts = blog_post_factory.create_batch(2, published=True, parent=blog, tags=2)

    url = blog.url + blog.reverse_subpage('by_tag', kwargs={'tag': 'test'})
    response = client.get(url)

    assert response.status_code == 200

    ctx = response.context_data

    assert ctx['page'] == blog
    assert len(ctx['posts']) == len(posts)

    for post in posts:
        assert post in ctx['posts']

    for post in excluded_posts:
        assert post not in ctx['posts']


@pytest.mark.parametrize('blog_post__published', [True])
@pytest.mark.parametrize('blog_post__parent', [LazyFixture('blog')])
def test_minimal_blog_post_page(client, blog_post):
    response = client.get(blog_post.url)

    assert response.status_code == 200
    assert response.context_data['page'] == blog_post


def test_full_blog_post_page(client, blog, blog_post_factory):
    post = blog_post_factory(parent=blog, full=True, published=True, owned=True, tags=2, categories=2)
    response = client.get(post.url)

    assert response.status_code == 200
    assert response.context_data['page'] == post
