from django import forms
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition


class WappsImage(AbstractImage):
    credit = models.CharField(_('Credit'), max_length=255, blank=True)
    credit_url = models.URLField(_('Credit URL'), max_length=255, blank=True)
    details = models.TextField(_('Details'), blank=True, null=True)

    admin_form_fields = Image.admin_form_fields + (
        'credit',
        'credit_url',
        'details',
    )


class WappsRendition(AbstractRendition):
    image = models.ForeignKey(WappsImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=WappsImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=WappsRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Do feature detection when a user saves an image without a focal point
@receiver(pre_save, sender=WappsImage)
def image_feature_detection(sender, instance, **kwargs):
    # Ensure feature dectection is enabled
    enabled = getattr(settings, 'WAGTAILIMAGES_FEATURE_DETECTION_ENABLED', False)
    # Make sure the image doesn't already have a focal point
    if enabled and not instance.has_focal_point():
        # Set the focal point
        instance.set_focal_point(instance.get_suggested_focal_point())
