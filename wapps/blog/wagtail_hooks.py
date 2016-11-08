from django.utils.translation import ugettext_lazy as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ThumbnailMixin, modeladmin_register as register_admin,
)
from wagtail.wagtailcore import hooks

from .models import Blog, BlogPost


@register_admin
class BlogPostAdmin(ThumbnailMixin, ModelAdmin):
    model = BlogPost
    menu_label = _('Blog')
    menu_icon = 'fa-rss'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('title', 'date', 'admin_thumb', 'owner')
    list_filter = ('date', 'tags', 'owner')
    search_fields = ('title', 'body')
    ordering = ('-date', )


@hooks.register('construct_main_menu')
def show_blog_only_if_page_present(request, menu_items):
    if Blog.objects.count() <= 0:
        menu_items[:] = [item for item in menu_items if item.name != 'blog']
