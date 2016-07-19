'''
Reusable image formats
'''
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailimages.formats import Format, register_image_format, unregister_image_format

# Override default formats
unregister_image_format('fullwidth')
unregister_image_format('left')
unregister_image_format('right')

FORMATS = {
    # Overriden formats
    'fullwidth': (_('Full width'), 'richtext-image full-width img-responsive', 'width-1000'),
    'left': (_('Left-aligned'), 'richtext-image left img-responsive', 'width-500'),
    'right': (_('Right-aligned'), 'richtext-image right img-responsive', 'width-500'),

    # Extras formats
    'centered': (_('Centered'), 'richtext-image full-width img-responsive', 'width-600'),
    'centered-portrait': (_('Centered portrait'), 'richtext-image full-width img-responsive', 'height-500'),
    'thumbnail': (_('Thumbnail'), 'richtext-image thumbnail', 'max-120x120'),
    'big-thumbnail': (_('Big thumbnail'), 'richtext-image thumbnail', 'max-240x240'),
}

for key, (label, classes, specs) in FORMATS.items():
    register_image_format(Format(key, label, classes, specs))
