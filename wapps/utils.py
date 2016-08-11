from django.conf import settings

from django.utils.functional import lazy
from django.utils.safestring import mark_safe

from wagtail.wagtailcore.models import PAGE_MODEL_CLASSES, Page

mark_safe_lazy = lazy(mark_safe, str)


def get_image_model():
    return getattr(settings, 'WAGTAILIMAGES_IMAGE_MODEL', 'wagtailimages.Image')


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
