from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from colorful.fields import RGBColorField

from wapps.mixins import SocialFields, ContactFields
from wapps.utils import mark_safe_lazy, get_image_model, get_image_url


@register_setting(icon='fa-universal-access')
class IdentitySettings(SocialFields, ContactFields, BaseSetting):
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

    amp_logo = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Mobile Logo'),
        help_text=mark_safe_lazy(_('An mobile optimized logo that must be 600x60'))
    )

    favicon = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Favicon'),
        help_text=mark_safe_lazy(_('The icon displayed in tab'))
    )

    favicon_large = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Large favicon'),
        help_text=mark_safe_lazy(_('The icon displayed on mobile device and desktop'))
    )

    svg_logo = models.FileField(_('SVG Logo'), null=True, blank=True)

    bg_color = RGBColorField(_('Background color'), default='#fff',
                             help_text=mark_safe_lazy(_('The background color used to tint the browser')))

    tags = TaggableManager(_('Tags'), blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('tags'),
        MultiFieldPanel([
            ImageChooserPanel('logo'),
            ImageChooserPanel('favicon'),
            ImageChooserPanel('favicon_large'),
            ImageChooserPanel('amp_logo'),
            FieldPanel('svg_logo'),
            FieldPanel('bg_color'),
        ], heading=_('Visual'), classname='collapsible'),
        MultiFieldPanel(SocialFields.panels, heading=_('Social networks'), classname='collapsible'),
        MultiFieldPanel(ContactFields.panels, heading=_('Contact'), classname='collapsible'),
    ]

    def favicon_url(self, width, height=None):
        height = height or width
        specs = 'fill-{width}x{height}'.format(width=width, height=height)
        if self.favicon and self.favicon.width >= width:
            image = self.favicon
        elif self.favicon_large:
            image = self.favicon_large
        elif self.logo:
            image = self.logo
        else:
            return
        return get_image_url(image, specs)
