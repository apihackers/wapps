import pytest

from wapps import jsonld


@pytest.mark.django_db
def test_minimal_blog(wrf, site, identity, blog):
    data = jsonld.graph({'request': wrf.get('/')}, blog)

    assert len(jsonld.extract(data['@graph'], 'Blog')) == 1
    graph = jsonld.extract_first(data['@graph'], 'Blog')

    assert graph['@id'] == blog.full_url
    assert graph['url'] == blog.full_url
    assert graph['name'] == blog.seo_title
    assert graph['description'] == blog.intro


@pytest.mark.django_db
def test_minimal_blogpost(wrf, site, identity, blog_post):
    data = jsonld.graph({'request': wrf.get('/')}, blog_post)

    assert len(jsonld.extract(data['@graph'], 'BlogPosting')) == 1
    graph = jsonld.extract_first(data['@graph'], 'BlogPosting')

    assert graph['@id'] == blog_post.full_url
    assert graph['url'] == blog_post.full_url
    assert graph['mainEntityOfPage'] == blog_post.full_url
    assert graph['name'] == blog_post.seo_title
    assert graph['description'] == blog_post.summarize(140)


@pytest.mark.django_db
def test_full_blogpost(wrf, site, identity, blog_post_factory):
    blog_post = blog_post_factory(full=True, owned=True, tags=3)
    data = jsonld.graph({'request': wrf.get('/')}, blog_post)

    assert len(jsonld.extract(data['@graph'], 'BlogPosting')) == 1
    graph = jsonld.extract_first(data['@graph'], 'BlogPosting')

    assert graph['@id'] == blog_post.full_url
    assert graph['url'] == blog_post.full_url
    assert graph['mainEntityOfPage'] == blog_post.full_url
    assert graph['name'] == blog_post.seo_title
    assert graph['description'] == blog_post.summarize(140)
    assert graph['keywords'] == ','.join(t.name for t in blog_post.tags.all())
    assert 'author' in graph
    assert graph['author']['@type'] == 'Person'
    assert graph['author']['name'] == blog_post.owner.get_full_name()
