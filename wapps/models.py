from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition

from .mixins import SocialFields
from .utils import mark_safe_lazy


@register_setting(icon='fa-universal-access')
class IdentitySettings(SocialFields, BaseSetting):
    class Meta:
        verbose_name = _('Identity')

    name = models.CharField(_('Name'), max_length=255, null=True, blank=True,
                            help_text=mark_safe_lazy(_('The entity public name')))

    description = models.TextField(_('Description'), max_length=255, null=True, blank=True,
                                  help_text=mark_safe_lazy(_('A short entity description')))

    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Logo'),
    )

    tags = TaggableManager(_('Tags'), blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('tags'),
        ImageChooserPanel('logo'),
        MultiFieldPanel(SocialFields.panels, heading=_('Social networks'), classname='collapsible'),
    ]


class WappsImage(AbstractImage):
    credit = models.CharField(_('Credit'), max_length=255, blank=True)
    credit_url = models.URLField(_('Credit URL'), max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'credit',
        'credit_url',
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
