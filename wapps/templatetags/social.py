from datetime import datetime

import jinja2
import requests

from django.utils.translation import ugettext_lazy as _
from django_jinja import library
from jinja2.ext import Extension
from memoize import memoize
from urllib.parse import quote_plus

from wapps import social
from wapps.utils import get_image_url


INSTAGRAM_IMAGE_SIZES = {
    'thumbnail': 'thumbnail',
    'low': 'low_resolution',
    'standard': 'standard_resolution',
}
INSTAGRAM_SIZES = {
    'thumbnail': 150,
    'low': 320,
    'standard': 640,
}
INSTAGRAM_DEFAULT_SIZE = 'thumbnail'
INSTAGRAM_DEFAULT_LENGTH = 10
INSTAGRAM_CACHE_TIMEOUT = 60 * 5  # Cache for 5 minutes
INSTAGRAM_FEED_PATTERN = 'https://www.instagram.com/{user}/media/'


@library.global_function
def social_url(network, value):
    return social.user_url(network, value)


@library.global_function
def social_icon(network):
    return social.icon(network)


@library.global_function
def social_share_url(network, url, title=None):
    return jinja2.Markup(social.share_url(network, url, title))


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
        'url': quote_plus(page.full_url),
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


def instagram_datetime(value):
    '''Parse an instagram feed datetime'''
    return datetime.fromtimestamp(int(value))


def instagram_error_response(size):
    return [{
        'id': 'unknown',
        'src': 'https://placehold.it/{size}x{size}/aaa/f00?text={text}'.format(
            size=INSTAGRAM_SIZES[size], text=_('Error'),
        ),
        'text': _('Error while fetching data'),
        'link': '#',
        'likes': 0,
        'comments': 0,
        'location': None,
        'date': datetime.now(),
    }]


@library.global_function
@memoize(timeout=INSTAGRAM_CACHE_TIMEOUT)
def instagram_feed(user, size=INSTAGRAM_DEFAULT_SIZE, length=INSTAGRAM_DEFAULT_LENGTH):
    if size not in INSTAGRAM_IMAGE_SIZES:
        raise ValueError('Unknown image size "{0}"'.format(size))
    url = INSTAGRAM_FEED_PATTERN.format(user=user)
    try:
        response = requests.get(url)
    except requests.RequestException:
        return instagram_error_response(size)
    if response.status_code != requests.codes.ok:
        return instagram_error_response(size)
    try:
        data = response.json()
    except ValueError:
        return instagram_error_response(size)
    image_size = INSTAGRAM_IMAGE_SIZES[size]

    return [{
        'id': i['id'],
        'src': i['images'][image_size]['url'],
        'text': i['caption']['text'],
        'link': i['link'],
        'likes': i['likes']['count'],
        'comments': i['comments']['count'],
        'location': (i['location'] or {}).get('name'),
        'date': instagram_datetime(i['created_time']),
    } for i in data['items'][:length]]
