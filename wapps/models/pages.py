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

from wapps.utils import get_image_model


class StaticPageTag(TaggedItemBase):
    content_object = ParentalKey('wapps.StaticPage', related_name='tagged_items')


class StaticPage(Page):
    intro = models.TextField(blank=True, null=True)
    body = RichTextField()
    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    image_full = models.BooleanField(_('Fully sized image'), default=False,
                                     help_text=_('Use the fully sized image'))

    tags = ClusterTaggableManager(through=StaticPageTag, blank=True)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('image_full'),
        ], heading=_('Main image'), classname='collapsible'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    class Meta:
        verbose_name = _('Static Page')

    def __jsonld__(self, context):
        request = context['request']
        data = {
            '@context': 'http://schema.org',
            '@type': 'Article',
            '@id': self.full_url,
            'name': self.seo_title or self.title,
            'datePublished': self.first_published_at.isoformat(),
            'dateModified': self.latest_revision_created_at.isoformat(),
            'headline': Truncator(strip_tags(self.search_description or str(self.intro))).chars(100),
            'articleBody': str(self.body),
            'author': {
                '@type': 'Person',
                'name': self.owner.get_full_name()
            },
        }
        if self.image:
            data['image'] = request.site.root_url + self.image.get_rendition('original').url
        return data
