from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel

from .mixins import SocialFields
from .utils import mark_safe_lazy


class IdentityTag(TaggedItemBase):
    content_object = ParentalKey('wapps.IdentitySettings', related_name='tagged_items')


@register_setting(icon='fa-universal-access')
class IdentitySettings(SocialFields, ClusterableModel, BaseSetting):
    class Meta:
        verbose_name = _('Identity')

    name = models.CharField(_('Name'), max_length=255, null=True, blank=True,
                            help_text=mark_safe_lazy(_('The entity public name')))

    description = models.TextField(_('Description'), max_length=255, null=True, blank=True,
                                  help_text=mark_safe_lazy(_('A short entity description')))

    tags = ClusterTaggableManager(_('Tags'), through=IdentityTag, blank=True)

    panels =  [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('tags'),
        MultiFieldPanel(SocialFields.panels, heading=_('Social networks'), classname='collapsible'),
    ]
