from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from wagtail.wagtailcore.models import Site

from wapps.templatetags.seo import Metadata
from wapps.utils import get_image_url
from wapps.models import IdentitySettings


class ExtendedAtomFeed(Atom1Feed):
    '''
    An Atom 1.0 feed augmented with the following namespaces:
     - content
     - media
     - webfeeds
    '''
    namespaces = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'media': 'http://search.yahoo.com/mrss/',
        'webfeeds': 'http://webfeeds.org/rss/1.0',
    }

    def root_attributes(self):
        attrs = super(ExtendedAtomFeed, self).root_attributes()
        attrs.update(('xmlns:{0}'.format(ns), url) for ns, url in self.namespaces.items())
        return attrs

    def add_root_elements(self, handler):
        super(ExtendedAtomFeed, self).add_root_elements(handler)

        if self.feed.get('image'):
            # Feedly cover image
            handler.addQuickElement('webfeeds:cover', '', {
                'image': get_image_url(self.feed['image'], 'fill-1920x1080'),
            })
        if self.feed.get('svg_logo'):
            # Feedly SVG Logo
            handler.addQuickElement('webfeeds:logo', self.feed['svg_logo'])
        if self.feed.get('favicon'):
            # Feedly Favicon
            handler.addQuickElement('webfeeds:icon', self.feed['favicon'])
        if self.feed.get('color'):
            # Feedly link color
            handler.addQuickElement('webfeeds:accentColor', '', {
                'image': self.feed['color'],
            })
        # Feedly related content
        handler.addQuickElement('webfeeds:related', '', {
            'layout': 'card',
            'target': 'browser',
        })
        if self.feed.get('googleanalytics_id'):
            # Feedly Google Analytics
            handler.addQuickElement('webfeeds:analytics', '', {
                'id': self.feed['googleanalytics_id'],
                'engine': 'GoogleAnalytics',
            })

    def cdata(self, handler, name, content, attrs=None):
        handler.startElement(name, attrs or {})
        cdata = '<![CDATA[{}]]>'.format(content or '')
        handler.ignorableWhitespace(cdata)
        handler.endElement(name)

    def add_item_elements(self, handler, item):
        super(ExtendedAtomFeed, self).add_item_elements(handler, item)

        if item.get('image'):
            handler.addQuickElement('media:content', '', {
                'url': get_image_url(item['image'], 'fill-1920x1080'),
                'type': 'image/png',
                'height': '1080',
                'width': '1920',
            })

        if item.get('content'):
            self.cdata(handler, 'content:encoded', item['content'])


class SiteFeed(Feed):
    feed_type = ExtendedAtomFeed

    def __call__(self, request, *args, **kwargs):
        self.request = request
        self.site = Site.find_for_request(self.request)
        self.identity = IdentitySettings.for_site(self.site)
        self.meta = Metadata(request=request, site=self.site, page=kwargs.get('page', None))
        return super().__call__(request, *args, **kwargs)

    def feed_extra_kwargs(self, obj):
        kwargs = super().feed_extra_kwargs(obj)
        if self.meta.image:
            kwargs['image'] = self.meta.image
        if self.identity.bg_color:
            kwargs['color'] = self.identity.bg_color
        if self.identity.favicon:
            kwargs['favicon'] = get_image_url(self.identity.favicon, 'fill-16x16')
        if self.identity.svg_logo:
            kwargs['svg_logo'] = self.identity.svg_logo.url
        if getattr(settings, 'GOOGLE_ANALYTICS_ID', None):
            kwargs['googleanalytics_id'] = settings.GOOGLE_ANALYTICS_ID
        return kwargs

    def item_extra_kwargs(self, item):
        kwargs = super(SiteFeed, self).item_extra_kwargs(item)
        kwargs.update(
            content=self.item_content(item),
            image=self.item_image(item),
        )
        return kwargs

    def item_content(self, item):  # pragma: nocover
        '''The full item HTML content'''
        pass

    def item_image(self, item):
        '''The full item HTML content'''
        if getattr(item, 'image', None):
            return item.image
        elif getattr(item, 'feed_image', None):
            return item.feed_image

    def title(self):
        return self.meta.site_title

    def link(self):
        return self.site.root_url
