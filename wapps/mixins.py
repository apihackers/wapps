from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from .utils import get_image_model


class LinkFields(models.Model):
    '''
    Link to either:
    * an internal page
    * an internal document
    * an external URL
    '''
    link_external = models.URLField(_('External link'), blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class AddressFields(models.Model):
    address_1 = models.CharField(_('Address'), max_length=255, blank=True)
    address_2 = models.CharField(_('Address (complement)'), max_length=255, blank=True)
    post_code = models.CharField(_('Postal code'), max_length=10, blank=True)
    city = models.CharField(_('City'), max_length=255, blank=True)
    country = models.CharField(_('Country'), max_length=255, blank=True)

    panels = [
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('post_code'),
        FieldPanel('city'),
        FieldPanel('country'),
    ]

    class Meta:
        abstract = True


class ContactFields(AddressFields):
    telephone = models.CharField(_('Telephone'), max_length=20, blank=True)
    email = models.EmailField(blank=True)

    panels = AddressFields.panels + [
        FieldPanel('telephone'),
        FieldPanel('email'),
    ]

    class Meta:
        abstract = True


class SocialFields(models.Model):
    '''Social networks links'''
    facebook = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255, blank=True)
    instagram = models.CharField(max_length=255, blank=True)
    pinterest = models.CharField(max_length=255, blank=True)
    youtube = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('facebook'),
        FieldPanel('twitter'),
        FieldPanel('linkedin'),
        FieldPanel('instagram'),
        FieldPanel('pinterest'),
        FieldPanel('youtube'),
    ]

    class Meta:
        abstract = True


class CarouselItem(LinkFields):
    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        verbose_name = _('Carousel item')
        verbose_name_plural = _('Carousel items')
        abstract = True


class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        verbose_name = _('Related link')
        verbose_name_plural = _('Related links')
        abstract = True


class TopImage(models.Model):
    top_image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('top_image'),
    ]

    class Meta:
        abstract = True


# @register_snippet
# class DefaultTopImage(models.Model):
#     default_top_image = models.ForeignKey(
#         'wagtailimages.Image'
#     )
#
#     panels = [
#         ImageChooserPanel('default_top_image'),
#     ]
#
#     def __str__(self):
#         return self.default_top_image.title
