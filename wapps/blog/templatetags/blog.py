import jinja2

from django_jinja import library

from wapps.templatetags.seo import Metadata

from ..models import Blog


@library.global_function
@library.render_with('blog/metadata.html')
@jinja2.contextfunction
def blog_meta(context):
    ctx = context.get_all()
    request = context['request']
    site = request.site
    ctx['blogs'] = (b for b in Blog.objects.live() if b.get_site().pk == site.pk)
    ctx['meta'] = Metadata(ctx)
    return ctx


@library.global_function
@jinja2.contextfunction
def blog_feed_url(context):
    request = context['request']
    site = request.site
    for blog in Blog.objects.live():
        if blog.get_site().pk == site.pk:
            return blog.full_url + blog.reverse_subpage('feed')
