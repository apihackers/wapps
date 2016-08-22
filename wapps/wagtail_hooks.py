from django.conf import settings
from django.utils.html import format_html_join
from wagtail.wagtailcore import hooks
from django.contrib.staticfiles.templatetags.staticfiles import static


@hooks.register('insert_editor_js')
def editor_js():
    js_files = []

    if 'word_count' in getattr(settings, 'WAPPS_FEATURES', []):
        js_files.append(static('wapps/hallo-counter.js'))

    if not js_files:
        return ''

    out = format_html_join('\n', '<script src="{0}"></script>', ([f] for f in js_files))
    return out
