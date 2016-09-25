import jinja2

from django_jinja import library

from wapps.templatetags.seo import Metadata

from ..models import Blog


@library.global_function
@library.render_with('blog/metadata.html')
@jinja2.contextfunction
def blog_meta(context):
    request = context['request']
    site = request.site
    for blog in Blog.objects.live():
        if blog.get_site().pk == site.pk:
            return {
                'blog': blog,
                'meta': Metadata(context)
            }
    return {}
