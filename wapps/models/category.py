from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class Category(models.Model):
    name = models.CharField(_('Name'), max_length=80, unique=True)
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children",
                               help_text=_('Categories allows to sort your content according a hierarchy'))
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)
