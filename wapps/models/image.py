from django.db import models
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
            ('image', 'filter_spec', 'focal_point_key'),
        )
