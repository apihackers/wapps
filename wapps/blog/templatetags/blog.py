import jinja2

from django.db.models import Count

from django_jinja import library

from wapps.metadata import Metadata
from wapps.models import Category
from wapps.templatetags.wagtail import routablepageurl
from wapps.utils import get_site

from ..models import Blog, BlogPost, BlogPostTag
from ..utils import get_blog_from_context


@library.global_function
@library.render_with('blog/metadata.html')
@jinja2.contextfunction
def blog_meta(context):
    ctx = context.get_all()
    request = context['request']
    site = get_site(request)
    ctx['blogs'] = [b for b in Blog.objects.live() if getattr(b.get_site(), 'pk', None) == site.pk]
    ctx['meta'] = Metadata(ctx)
    return ctx


@library.global_function
@jinja2.contextfunction
def blog_feed_url(context):
    blog = get_blog_from_context(context)
    if blog:
        return blog.full_url + blog.reverse_subpage('feed')


@library.global_function
@jinja2.contextfunction
def blog_tags(context):
    blog = get_blog_from_context(context)
    if not blog:
        return []
    return BlogPostTag.tags_for(BlogPost).annotate(
        posts_count=Count('taggit_taggeditem_items')
    ).order_by('-posts_count')


@library.global_function
@jinja2.contextfunction
def blog_categories(context):
    blog = get_blog_from_context(context)
    if not blog:
        return []
    return Category.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        posts_count=Count('blogpost'),
    )


@library.global_function
@jinja2.contextfunction
def blog_latest_posts(context):
    blog = get_blog_from_context(context)
    if not blog:
        return []
    return blog.get_queryset()


@library.global_function
@jinja2.contextfunction
def blog_url(context, *args, **kwargs):
    blog = get_blog_from_context(context)
    if blog:
        return routablepageurl(context, blog, *args, **kwargs)
