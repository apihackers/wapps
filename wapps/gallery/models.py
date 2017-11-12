from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages import get_image_model, get_image_model_string
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wapps.utils import get_image_url

ImageModel = get_image_model_string()


class Gallery(Page):
    intro = RichTextField(_('Introduction'), blank=True,
                          help_text=_('A text to be displayed before albums'))

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    feed_image = models.ForeignKey(
        ImageModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def children(self):
        return self.get_children().live().specific()

    def get_context(self, request):
        # Get list of live Gallery pages that are descendants of this page
        pages = Album.objects.live().descendant_of(self)

        # Update template context
        context = super(Gallery, self).get_context(request)
        context['pages'] = pages
        context['albums'] = pages

        return context

    class Meta:
        verbose_name = _('Gallery')

    type_icon = 'fa-picture-o'
    subpage_types = [
        'gallery.Album',
        'gallery.ManualAlbum'
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full")
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, _('SEO and metadata')),
        ImageChooserPanel('feed_image'),
    ]

    def __jsonld__(self, context):
        request = context['request']
        data = {
            '@type': 'CollectionPage',
            '@id': self.full_url,
            'url': self.full_url,
            'name': self.seo_title or self.title,
        }
        if self.first_published_at:
            data.update({
                'datePublished': self.first_published_at.isoformat(),
                'dateModified': self.last_published_at.isoformat(),
            })
        if self.feed_image:
            data['image'] = request.site.root_url + self.feed_image.get_rendition('original').url

        data['hasPart'] = [album.__jsonld__(context) for album in self.children]

        return data


class AlbumTag(TaggedItemBase):
    content_object = ParentalKey(
        'gallery.Album', related_name='tagged_items'
    )


class Album(Page):
    tags = ClusterTaggableManager(through=AlbumTag, blank=True)

    intro = RichTextField(_('Introduction'), blank=True,
                          help_text=_('A text to be displayed before images'))

    show_details = models.BooleanField(_('Display details'), default=True,
                                       help_text=_('Display image title and details'))

    ANIMATIONS_TYPES = [
        ('slide', _('Slide')),
        ('fade', _('Fade')),
    ]

    animation = models.CharField(_('Animation'), max_length=8, choices=ANIMATIONS_TYPES, default='slide')

    image = models.ForeignKey(
        ImageModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Image'),
        help_text=_('The image seen on gallery browser and when sharing this album')
    )

    @property
    def gallery(self):
        # Find closest ancestor which is a Gallery index
        return self.get_ancestors().type(Gallery).specific().last()

    def get_context(self, request):
        context = super(Album, self).get_context(request)
        context['images'] = self.get_images(request)
        return context

    def get_images(self, request):
        tags = self.tags.all()

        # Be compatible with swappable image model
        model = get_image_model()

        # Creating empty Queryset from Wagtail image model
        return model.objects.filter(tags__in=tags).distinct()

    class Meta:
        verbose_name = _('Album')

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro'),
        FieldPanel('tags'),
        MultiFieldPanel([
            FieldPanel('show_details'),
            FieldPanel('animation'),
        ], _('Options')),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, _('SEO and metadata')),
        ImageChooserPanel('image'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    # parent_page_types = []
    subpage_types = []
    type_icon = 'fa-picture-o'

    def __jsonld__(self, context):
        request = context['request']
        data = {
            '@type': 'ImageGallery',
            '@id': self.full_url,
            'url': self.full_url,
            'name': self.seo_title or self.title,
            'associatedMedia': []
        }
        if self.first_published_at:
            data.update({
                'datePublished': self.first_published_at.isoformat(),
                'dateModified': self.latest_revision_created_at.isoformat(),
            })
        if self.image:
            data['image'] = request.site.root_url + self.image.get_rendition('original').url

        for image in self.get_images(request):
            image = getattr(image, 'image', image)
            media = {
                '@type': 'ImageObject',
                'name': image.title,
                'contentUrl': get_image_url(image, 'original'),
                'thumbnail': {
                    '@type': 'ImageObject',
                    'contentUrl': get_image_url(image, 'fill-300x300'),
                    'width': 300,
                    'height': 300,
                }
            }
            if image.details:
                media['description'] = image.details

            data['associatedMedia'].append(media)

        return data


class ManualAlbumImage(Orderable, models.Model):
    page = ParentalKey('gallery.ManualAlbum', related_name='images')
    image = models.ForeignKey(
        ImageModel,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class ManualAlbum(Album):
    def get_images(self, request):
        return [i.image for i in self.images.all()]

    class Meta:
        verbose_name = _('Manual album')

    template = 'gallery/album.html'
    content_panels = Album.content_panels + [
        InlinePanel('images', label=_('Images')),
    ]
