from django.apps import apps
from django.db import models
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
# from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wapps.utils import get_image_model, get_image_url

ImageModel = get_image_model()


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
        return self.get_children().live()

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
        return self.get_ancestors().type(Gallery).last()

    def get_context(self, request):
        context = super(Album, self).get_context(request)
        context['images'] = self.get_images(request)
        return context

    def get_images(self, request):
        # Get tags and convert them into list so we can iterate over them
        tags = self.tags.values_list('name', flat=True)

        # Be compatible with swappable image model
        model = apps.get_model(*ImageModel.split('.'))

        # Creating empty Queryset from Wagtail image model
        images = model.objects.none()

        if tags:
            for i in range(0, len(tags)):
                img = model.objects.filter(tags__name=tags[i])
                images = images | img

        return images

        # Pagination
        # page = request.GET.get('page')
        # paginator = Paginator(images, 20)  # Show 20 images per page
        # try:
        #     images = paginator.page(page)
        # except PageNotAnInteger:
        #     images = paginator.page(1)
        # except EmptyPage:
        #     images = paginator.page(paginator.num_pages)
        # return images

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

    def __jsonld__(self, context):
        request = context['request']
        data = {
            '@context': 'http://schema.org',
            '@type': 'ImageGallery',
            '@id': self.full_url,
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
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class ManualAlbum(Album):
    def get_images(self, request):
        # Creating empty Queryset from Wagtail image model
        images = self.images.all()

        # Pagination
        # page = request.GET.get('page')
        # paginator = Paginator(images, 20)  # Show 20 images per page
        # try:
        #     images = paginator.page(page)
        # except PageNotAnInteger:
        #     images = paginator.page(1)
        # except EmptyPage:
        #     images = paginator.page(paginator.num_pages)
        return images

    class Meta:
        verbose_name = _('Manual album')

    template = 'gallery/album.html'
    content_panels = Album.content_panels + [
        InlinePanel('images', label=_('Images')),
    ]
