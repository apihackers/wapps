import jinja2

from urllib.parse import quote_plus
from django_jinja import library

from jinja2.ext import Extension

from wapps.utils import get_image_url

from wapps import social


@library.global_function
def social_url(network, value):
    return social.user_url(network, value)


@library.global_function
def social_icon(network):
    return social.icon(network)


@library.global_function
def social_share_url(network, url, title=None):
    return social.share_url(network, url, title)


@library.global_function
@jinja2.contextfunction
def social_share_urls(context, page):
    request = context['request']
    data = []
    if page.image:
        image = request.site.root_url + get_image_url(page.image, 'original')
    else:
        image = None
    params = {
        'url': quote_plus(page.url),
        'title': quote_plus(page.seo_title or page.title),
        'image': image
    }
    for network, attrs in social.NETWORKS.items():
        if 'share' in attrs:
            shareurl = attrs['share'].format(**params)
            data.append((attrs['name'], shareurl, attrs.get('icon')))
    return data


@library.extension
class SocialSettings(Extension):
    def __init__(self, environment):
        super(SocialSettings, self).__init__(environment)
        environment.globals['SOCIAL_NETWORKS'] = social.NETWORKS.keys()
