import re

from datetime import date

from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.utils.pagination import paginate

from wapps import jsonld
from wapps.models import Category, IdentitySettings
from wapps.mixins import RelatedLink
from wapps.utils import get_image_model

from .feeds import BlogFeed

ImageModel = get_image_model()

DEFAULT_PAGE_SIZE = 10


class Blog(RoutablePageMixin, Page):
    '''
    A blog root page handling article querying and listing
    '''
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    image = models.ForeignKey(
        ImageModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('image'),
    ]

    promote_panels = Page.promote_panels

    def get_queryset(self):
        # Get list of live blog posts that are descendants of this page
        qs = BlogPost.objects.live().descendant_of(self)

        # Order by most recent date first
        qs = qs.order_by('-date')

        return qs

    @property
    def queryset(self):
        return self.get_queryset()

    @property
    def recents(self):
        return self.get_queryset()

    def get_context(self, request):
        context = super(Blog, self).get_context(request)

        _, posts = paginate(request, self.posts, 'page', DEFAULT_PAGE_SIZE)
        context['posts'] = posts
        return context

    @property
    def posts_with_image(self):
        return self.queryset.filter(image__isnull=False)

    @route(r'^$')
    def all_posts(self, request, *args, **kwargs):
        self.posts = self.get_queryset()
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.posts = self.queryset.filter(first_published_at__year=year)
        self.filter_type = _('date')
        self.filter_term = year
        if month:
            self.posts = self.posts.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.filter_term = df.format('F Y')
        if day:
            self.posts = self.posts.filter(date__day=day)
            self.filter_term = date_format(date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^tag/(?P<tag>[-_\w]+)/$')
    def by_tag(self, request, tag, *args, **kwargs):
        self.filter_type = _('tag')
        self.filter_term = tag
        self.posts = self.queryset.filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def by_category(self, request, category, *args, **kwargs):
        self.filter_type = _('category')
        self.filter_term = category
        self.posts = self.queryset.filter(blogpost_categories__category__slug=category)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^author/(?P<author>[-_\w]+)/$')
    def by_author(self, request, author, *args, **kwargs):
        self.filter_type = _('author')
        self.filter_term = author
        self.posts = self.queryset.filter(owner__username=author)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^feed/$')
    def feed(self, request, *args, **kwargs):
        feed = BlogFeed(self)
        return feed(request, *args, **kwargs)

    subpage_types = ['blog.BlogPost']

    def __jsonld__(self, context):
        now = timezone.now()
        data = {
            '@type': 'Blog',
            '@id': self.full_url,
            'url': self.full_url,
            'name': self.seo_title or self.title,
            'datePublished': (self.first_published_at or now).isoformat(),
            'dateModified': (self.last_published_at or now).isoformat(),
            'description': strip_tags(self.intro),
        }
        return data


class BlogPostRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('blog.BlogPost', related_name='related_links')


class BlogPostCategory(models.Model):
    category = models.ForeignKey(Category, related_name="+", verbose_name=_('Category'))
    page = ParentalKey('BlogPost', related_name='blogpost_categories')
    panels = [
        FieldPanel('category'),
    ]


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPost', related_name='tagged_items')


class BlogPost(Page):
    '''
    A single blog post (aka. article) page
    '''
    class Meta:
        verbose_name = _('Blog post')
        verbose_name_plural = _('Blog posts')

    body = RichTextField(verbose_name=_('body'))
    excerpt = models.CharField(verbose_name=_('excerpt'), blank=True, max_length=255,
                               help_text=_("Entry excerpt to be displayed on entries list. "
                                           "If this field is not filled, a truncate version "
                                           "of body text will be used."))

    date = models.DateTimeField(verbose_name=_('Post date'), default=timezone.now)

    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    categories = models.ManyToManyField(Category, through=BlogPostCategory, blank=True)

    image = models.ForeignKey(
        ImageModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('excerpt'),
        index.FilterField('page_ptr_id')
    ]

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            ImageChooserPanel('image'),
            FieldPanel('excerpt', classname="full"),
            FieldPanel('body', classname="full"),
        ], heading=_('Content')),
        MultiFieldPanel([
            FieldPanel('tags'),
            InlinePanel('blogpost_categories', label=_('Categories')),
            InlinePanel('related_links', label=_('Related links')),
        ], heading=_('Metadata')),
    ]

    # Page promote_panels without show in menu
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], _('Common page configuration')),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
        FieldPanel('owner'),
    ]
    #  settings_panels = [
    #     MultiFieldPanel([
    #         FieldRowPanel([
    #             FieldPanel('go_live_at'),
    #             FieldPanel('expire_at'),
    #         ], classname="label-above"),
    #     ], 'Scheduled publishing', classname="publishing"),
    #     FieldPanel('date'),
    #     FieldPanel('author'),
    # ]

    parent_page_types = ['blog.Blog']
    subpage_types = []
    type_icon = 'fa-rss-square'

    @property
    def blog(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(Blog).last().specific

    def summarize(self, length=255):
        text = self.excerpt or self.search_description or self.body
        return Truncator(strip_tags(str(text))).chars(length)

    def __jsonld__(self, context):
        request = context['request']
        site = request.site
        identity = IdentitySettings.for_site(site)
        body = str(self.body)
        now = timezone.now()
        publisher = jsonld.organization(context)
        if identity.amp_logo:
            publisher['logo'] = jsonld.image_object(context, identity.amp_logo, 600, 60)
        data = {
            '@type': 'BlogPosting',
            '@id': self.full_url,
            'url': self.full_url,
            'mainEntityOfPage': self.full_url,
            'name': self.seo_title or self.title,
            'datePublished': (self.date or now).isoformat(),
            'dateModified': (self.latest_revision_created_at or now).isoformat(),
            'headline': self.excerpt,
            'keywords': ','.join(t.name for t in self.tags.all()),
            'articleBody': body,
            'description': self.summarize(140),
            'wordCount': len(re.findall(r'\w+', strip_tags(body))),
            'publisher': publisher,
        }
        if self.owner:
            data['author'] = {
                '@type': 'Person',
                'name': self.owner.get_full_name()
            }
        if self.image:
            # According to https://developers.google.com/+/web/snippet/article-rendering
            # Image must had a ratio between 5:2 and 5:3
            data['image'] = jsonld.image_object(context, self.image, 1000, 600)
        return data


BlogPost._meta.get_field('owner').editable = True


class BlogBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'), required=False)
    nb_articles = blocks.IntegerBlock(label=_('Number of articles'), default=3)

    def get_context(self, value, parent_context=None):
        from .utils import get_blog_from_context
        context = super(BlogBlock, self).get_context(value, parent_context=parent_context)
        context['blog'] = get_blog_from_context(parent_context or {})
        return context

    class Meta:
        label = _('Blog')
        icon = 'fa-rss'
        template = 'blog/blog-block.html'
