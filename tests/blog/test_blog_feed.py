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
