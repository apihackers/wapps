import jinja2

from urllib.parse import quote_plus
from django_jinja import library

from jinja2.ext import Extension


NETWORKS = {
    'twitter': {
        'name': 'Twitter',
        'icon': 'fa-twitter',
        'url': 'https://twitter.com/{user}',
        'share': 'https://twitter.com/share?url={url}&text={title}',
    },
    'linkedin': {
        'name': 'LinkedIn',
        'icon': 'fa-linkedin',
        'url': 'https://twitter.com/{user}',
        'url': 'http://www.linkedin.com/shareArticle?url={url}&title={title}',
    },
    'facebook': {
        'name': 'Facebook',
        'icon': 'fa-facebook',
        'url': 'https://facebook.com/{user}',
        'share': 'http://www.facebook.com/sharer.php?u={url}',
    },
    'google': {
        'name': 'Google',
        'share': 'https://plus.google.com/share?url={url}',
    },
    'instagram': {
        'name': 'Instagram',
        'icon': 'fa-instagram',
        'url': 'https://www.instagram.com/{user}',
    },
    'pinterest': {
        'name': 'PInterest',
        'icon': 'fa-pinterest',
        'url': 'https://pinterest.com/{user}',
        'share': ('https://pinterest.com/pin/create/bookmarklet/'
                  '?media={image}&url={url}&description={title}'),
    },
    'reddit': {
        'name': 'Reddit',
        'share': 'http://reddit.com/submit?url={url}&title={title}',
    },
    'email': {
        'name': 'email',
        'icon': 'fa-envelope',
        'url': 'mailto:{user}',
        'share': 'mailto:?subject={title}&body={url}',
    },
}


def get_network(name):
    if name not in NETWORKS:
        raise ValueError('Unknown social network "{name}"'.format(name=name))
    return NETWORKS[name]


@library.global_function
def social_url(network, value):
    return get_network(network)['url'].format(user=value)


@library.global_function
def social_icon(network):
    return get_network(network).get('icon')


@library.global_function
def social_share_url(network, url, title=None):
    template = get_network(network).get('share')
    if template:
        return template.format(url=url, title=title)


@library.global_function
@jinja2.contextfunction
def social_share_urls(context, page):
    request = context['request']
    data = []
    if page.image:
        image = request.site.root_url + page.image.get_rendition('original').url
    else:
        image = None
    params = {
        'url': quote_plus(page.url),
        'title': quote_plus(page.seo_title or page.title),
        'image': image
    }
    for network, attrs in NETWORKS.items():
        if 'share' in attrs:
            shareurl = attrs['share'].format(**params)
            data.append((attrs['name'], shareurl, attrs.get('icon')))
    return data


@library.extension
class SocialSettings(Extension):
    def __init__(self, environment):
        super(SocialSettings, self).__init__(environment)
        environment.globals['SOCIAL_NETWORKS'] = NETWORKS.keys()
