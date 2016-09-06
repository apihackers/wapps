import jinja2

from django_jinja import library

from ..models import IdentitySettings


class Metadata(object):
    '''
    Extract metadata from a Page object
    '''
    def __init__(self, context, **kwargs):
        self.context = context
        self.kwargs = kwargs
        self.page = context.get('page', None)
        self.request = context['request']
        self.site = self.request.site
        self.identity = IdentitySettings.for_site(self.site)

    @property
    def title(self):
        if self.kwargs.get('title'):
            return self.kwargs['title']
        elif self.page:
            return self.page.seo_title or self.page.title

    @property
    def site_title(self):
        return self.identity.name or self.context.get('WAGTAIL_SITE_NAME')

    @property
    def full_title(self):
        if self.site_title and self.title:
            return ' | '.join((self.title, self.site_title))
        elif self.site_title:
            return self.site_title
        elif self.title:
            return self.title

    @property
    def description(self):
        if self.kwargs.get('description'):
            return self.kwargs['description']
        elif getattr(self.page, 'search_description', None):
            return self.page.search_description
        elif getattr(self.page, 'description', None):
            return self.page.description
        else:
            return self.identity.description

    @property
    def image(self):
        if self.kwargs.get('image'):
            return self.kwargs['image']
        elif getattr(self.page, 'feed_image', None):
            return self.site.root_url + self.page.feed_image.get_rendition('original').url
        elif getattr(self.page, 'image', None):
            return self.site.root_url + self.page.image.get_rendition('original').url
        elif self.identity.logo:
            return self.site.root_url + self.identity.logo.get_rendition('original').url

    @property
    def tags(self):
        tags = set(self.identity.tags.all())
        if self.kwargs.get('tags'):
            tags.update(self.kwargs['tags'])
        if getattr(self.page, 'tags', None):
            tags.update(self.page.tags.all())
        return tags


@library.global_function
@jinja2.contextfunction
def page_meta(context, **kwargs):
    return Metadata(context, **kwargs)
