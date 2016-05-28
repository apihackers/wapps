from django.utils.translation import ugettext_lazy as _

from django_jinja import library

from jinja2.ext import Extension


SOCIAL_URLS = {
    'twitter': 'https://twitter.com/{user}',
    'linkedin': 'https://twitter.com/{user}',
    'facebook': 'https://facebook.com/{user}',
    'instagram': 'https://www.instagram.com/{user}',
    'pinterest': 'https://pinterest.com/{user}',
    'email': 'mailto:{user}',
}


@library.global_function
def social_url(network, value):
    if network not in SOCIAL_URLS:
        return value
    return SOCIAL_URLS[network].format(user=value)


@library.global_function
def social_icon(network):
    if network == 'email':
        return 'fa-envelope'
    return 'fa-{0}'.format(network)


@library.extension
class SocialSettings(Extension):
    def __init__(self, environment):
        super(SocialSettings, self).__init__(environment)
        environment.globals['SOCIAL_NETWORKS'] = SOCIAL_URLS.keys()
