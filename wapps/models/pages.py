from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.utils.text import Truncator

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wapps.utils import get_image_model, get_site


class StaticPageTag(TaggedItemBase):
    content_object = ParentalKey('wapps.StaticPage', related_name='tagged_items')


class StaticPage(Page):
    intro = models.TextField(_('Introduction'), blank=True, null=True,
                             help_text=_('An optional introduction used as page heading and summary'))
    body = RichTextField(_('Body'),
                         help_text=_('The main page content'))
    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('The main page image (seen when shared)')
    )

    image_full = models.BooleanField(_('Fully sized image'), default=False,
                                     help_text=_('Use the fully sized image'))

    SEO_TYPES = [
        ('article', _('Article')),
        ('service', _('Service')),
        ('faq', _('FAQ')),
    ]

    seo_type = models.CharField(_('Search engine type'), max_length=10,
                                choices=SEO_TYPES, default='article',
                                help_text=_('What does this page represents'))

    tags = ClusterTaggableManager(through=StaticPageTag, blank=True)

    content_panels = [
        FieldPanel('title', classname="full title"),
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('image_full'),
        ], heading=_('Main image'), classname='collapsible'),
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
        FieldPanel('seo_type')
    ]

    type_icon = 'fa-file-text-o'

    class Meta:
        verbose_name = _('Static Page')

    def __jsonld__(self, context):
        request = context['request']
        data = {
            '@id': self.full_url,
            'url': self.full_url,
            'name': self.seo_title or self.title,
        }
        tags = self.tags.all()
        if tags:
            data['keywords'] = ','.join(t.name for t in tags)
        if self.image:
            data['image'] = get_site(request).root_url + self.image.get_rendition('original').url

        jsonld_method_name = 'get_jsonld_{0}'.format(self.seo_type)
        jsonld_method = getattr(self, jsonld_method_name, None)
        if jsonld_method:
            data = jsonld_method(context, data)

        return data

    def get_jsonld_article(self, context, data):
        data.update({
            '@type': 'Article',
            'headline': Truncator(strip_tags(self.search_description or str(self.intro))).chars(100),
            'articleBody': str(self.body),
        })
        if self.first_published_at:
            data.update({
                'datePublished': self.first_published_at.isoformat(),
                'dateModified': self.last_published_at.isoformat(),
            })
        if self.owner:
            data.update(author={
                '@type': 'Person',
                'name': self.owner.get_full_name()
            })
        return data

    def get_jsonld_service(self, context, data):
        data.update({
            '@type': 'Service',
        })
        return data

    def get_jsonld_faq(self, context, data):
        data.update({
            '@type': 'FAQPage',
            'headline': Truncator(strip_tags(self.search_description or str(self.intro))).chars(100),
        })
        if self.first_published_at:
            data.update({
                'datePublished': self.first_published_at.isoformat(),
                'dateModified': self.last_published_at.isoformat(),
            })
        if self.owner:
            data.update(author={
                '@type': 'Person',
                'name': self.owner.get_full_name()
            })
        return data
