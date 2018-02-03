import pytest

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures('site'),
]


@pytest.mark.parametrize('blog__published', [True])
def test_blog_feed_url(jinja, wrf, blog):
    assert jinja('{{ blog_feed_url() }}', request=wrf.get('/')) == blog.full_url + blog.reverse_subpage('feed')


def test_blog_feed_url_no_blog(jinja, wrf):
    assert jinja('{{ blog_feed_url() }}', request=wrf.get('/')) == 'None'


@pytest.mark.parametrize('blog__published', [True])
def test_blog_url(jinja, wrf, blog):
    expected = blog.url + blog.reverse_subpage('by_tag', kwargs={'tag': 'tag'})
    assert jinja('{{ blog_url("by_tag", tag="tag") }}', request=wrf.get('/')) == expected


def test_blog_url_no_blog(jinja, wrf):
    assert jinja('{{ blog_url("by_tag", tag="tag") }}', request=wrf.get('/')) == 'None'
