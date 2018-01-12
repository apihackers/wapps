import hashlib
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.utils.safestring import mark_safe

from wagtail.wagtailcore.models import PAGE_MODEL_CLASSES, Page, Site


mark_safe_lazy = lazy(mark_safe, str)


def get_image_model():
    return getattr(settings, 'WAGTAILIMAGES_IMAGE_MODEL', 'wagtailimages.Image')


def get_site(request):
    return getattr(request, 'site', Site.objects.get(is_default_site=True))


def get_image_url(image, filter_spec):
    from wagtail.wagtailimages.views.serve import generate_signature

    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    # Append image's original filename to the URL (optional)
    url += image.file.name[len('original_images/'):]

    return url


def hide_page_type(cls):
    ''''Hide a page type from creation'''
    if cls in PAGE_MODEL_CLASSES:
        PAGE_MODEL_CLASSES.remove(cls)


def hide_parent_type(cls):
    '''
    Hide parent page type from creation
    '''
    for parent in cls.__bases__:
        if issubclass(parent, Page):
            hide_page_type(parent)
            break  # Can only inherit from one page model
    return cls


def timehash(length=10):
    '''Generate a time-based hash'''
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    return hash.hexdigest()[:length]
