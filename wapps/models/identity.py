from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wapps.mixins import SocialFields
from wapps.utils import mark_safe_lazy, get_image_model


@register_setting(icon='fa-universal-access')
class IdentitySettings(SocialFields, BaseSetting):
    class Meta:
        verbose_name = _('Identity')

    name = models.CharField(_('Name'), max_length=255, null=True, blank=True,
                            help_text=mark_safe_lazy(_('The entity public name')))

    description = models.TextField(_('Description'), max_length=255, null=True, blank=True,
                                  help_text=mark_safe_lazy(_('A short entity description')))

    logo = models.ForeignKey(
        get_image_model(),
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
