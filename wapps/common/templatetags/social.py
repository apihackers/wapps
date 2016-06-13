from django_jinja import library

from jinja2.ext import Extension


NETWORKS = {
    'twitter': {
        'name': 'Twitter',
        'icon': 'fa-twitter',
        'url': 'https://twitter.com/{user}',
    },
    'linkedin': {
        'name': 'LinkedIn',
        'icon': 'fa-linkedin',
        'url': 'https://twitter.com/{user}',
    },
    'facebook': {
        'name': 'Facebook',
        'icon': 'fa-facebook',
        'url': 'https://facebook.com/{user}',
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
    },
    'email': {
        'name': 'email',
        'icon': 'fa-envelope',
        'url': 'mailto:{user}',
    }
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
    return get_network(network)['icon']


@library.extension
class SocialSettings(Extension):
    def __init__(self, environment):
        super(SocialSettings, self).__init__(environment)
        environment.globals['SOCIAL_NETWORKS'] = NETWORKS.keys()
