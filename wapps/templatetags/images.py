import jinja2

from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from django.utils.translation import ugettext as _
from django_jinja import library

from wapps.models import IdentitySettings

PLACEHOLDIT_URL = 'https://placehold.it/{width}x{height}/{bg}/{fg}?text={text}'

DEFAULT_BACKGROUND = '#ccc'
DEFAULT_FOREGROUND = '#969696'


@library.filter
@jinja2.contextfilter
def placeholder(ctx, value, width, height, bg=None, fg=None, text=None, site=True, **kwargs):
    '''
    A placehold.it fallback filter or global function.

    Try ``IdentitySettings.name`` then fallback on ``Site.name`` for text.
    You can disable this behavior with `site=False` parameter,
    then the dimensions will be used as text.
    You can override the text with `text='My text'` parameter or configuration.

    All parameters default can be set in your settings::

        WAPPS_PLACEHOLDER = {
            'fg': '#0aa',
            'bg': '#aaa',
            'text': 'Placeholder',
        }

    '''
    if value:
        return value
    placeholder_settings = getattr(settings, 'WAPPS_PLACEHOLDER', {})
    params = {
        'width': width,
        'height': height,
        'fg': fg or placeholder_settings.get('fg', DEFAULT_FOREGROUND),
        'bg': bg or placeholder_settings.get('bg', DEFAULT_BACKGROUND),
    }
    if not text:
        request = ctx['request']
        site = request.site
        if site:
            identity = IdentitySettings.for_site(site)
            text = getattr(identity, 'name') or site.site_name
    if not text:
        text = '{width}x{height}'.format(**params)
    params['text'] = text.replace(' ', '+')
    for key in 'fg', 'bg':
        params[key] = params[key].replace('#', '')
    url = PLACEHOLDIT_URL.format(**params)

    if value == '':
        # Empty image() call, expect an <img/> tag
        attrs = {
            'src': url,
            'title': text,
            'alt': _('Placeholder'),
            'width': params['width'],
            'height': params['height'],
        }
        attrs.update(**kwargs)
        return mark_safe('<img {0}/>'.format(flatatt(attrs)))
    else:
        # This is an undefined url
        return url
