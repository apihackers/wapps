from urllib.parse import quote_plus


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
        'url': 'https://www.linkedin.com/in/{user}',
        'share': 'https://www.linkedin.com/shareArticle?url={url}&title={title}',
    },
    'facebook': {
        'name': 'Facebook',
        'icon': 'fa-facebook',
        'url': 'https://facebook.com/n/?{user}',
        'share': 'https://www.facebook.com/sharer.php?u={url}',
    },
    'google': {
        'name': 'Google',
        'share': 'https://plus.google.com/share?url={url}',
    },
    'instagram': {
        'name': 'Instagram',
        'icon': 'fa-instagram',
        'url': 'https://instagram.com/_u/{user}',
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
        'icon': 'fa-reddit',
        'share': 'https://reddit.com/submit?url={url}&title={title}',
    },
    'email': {
        'name': 'email',
        'icon': 'fa-envelope',
        'url': 'mailto:{user}',
        'share': 'mailto:?subject={title}&body={url}',
    },
    'youtube': {
        'name': 'YouTube',
        'icon': 'fa-youtube',
        'url': 'https://www.youtube.com/user/{user}',
    }
}


def network(name):
    if name not in NETWORKS:
        raise ValueError('Unknown social network "{name}"'.format(name=name))
    return NETWORKS[name]


def user_url(network_name, value):
    if value.startswith('http://'):
        return value.replace('http://', 'https://')
    elif value.startswith('https://'):
        return value
    return network(network_name).get('url', '').format(user=value)


def icon(network_name):
    return network(network_name).get('icon')


def share_url(network_name, url, title=None):
    template = network(network_name).get('share')
    if template:
        title = quote_plus(title) if title else None
        return template.format(url=quote_plus(url), title=title)
