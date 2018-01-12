from .models import Blog


def get_site_blog(site):
    for blog in Blog.objects.live():
        if site.root_page in blog.get_ancestors():
            return blog


def get_blog_from_context(context):
    request = context['request']
    site = request.site
    return get_site_blog(site)
