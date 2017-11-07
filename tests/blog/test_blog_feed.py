import pytest

import feedparser


@pytest.mark.django_db
@pytest.mark.parametrize('blog__published', [True])
def test_minimal_blog_feed(client, site, identity, blog):
    url = blog.url + blog.reverse_subpage('feed')
    response = client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'].split(';', 1)[0] == 'application/atom+xml'

    d = feedparser.parse(response.content)
    assert d.feed.title == ' » '.join((identity.name, blog.title))
    assert len(d.entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize('blog__published', [True])
def test_full_blog_feed(client, site, full_identity, blog, blog_post_factory):
    posts = blog_post_factory.create_batch(3, parent=blog, published=True)
    url = blog.url + blog.reverse_subpage('feed')
    response = client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'].split(';', 1)[0] == 'application/atom+xml'

    d = feedparser.parse(response.content)
    assert d.feed.title == ' » '.join((full_identity.name, blog.title))
    assert len(d.entries) == len(posts)


@pytest.mark.django_db
@pytest.mark.parametrize('blog__published', [True])
def test_non_published_posts_are_hidden(client, site, identity, blog, blog_post_factory):
    posts = blog_post_factory.create_batch(3, parent=blog)
    for post in posts:
        assert not post.live
    url = blog.url + blog.reverse_subpage('feed')
    response = client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'].split(';', 1)[0] == 'application/atom+xml'

    d = feedparser.parse(response.content)
    assert d.feed.title == ' » '.join((identity.name, blog.title))
    assert len(d.entries) == 0
