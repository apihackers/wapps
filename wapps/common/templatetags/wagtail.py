import jinja2

from django.conf import settings
from django.template.loader import get_template
from django_jinja import library
from jinja2.ext import Extension
from wagtail.wagtailcore.models import Page


@library.global_function
def menu():
    return Page.objects.live().in_menu().filter(depth__lte=3)


@library.global_function
@jinja2.contextfunction
def render_stream(context, stream_child):
    # Use the django_jinja to get the template content based on its name
    template = get_template(stream_child.block.meta.template)
    # Create a new context based on the current one as we can't edit it directly
    new_context = context.get_all()
    # Add the value on the context (value is the keyword chosen by wagtail for the blocks context)
    new_context.update(stream_child.block.get_context(stream_child.value))
    # Render the template with the context
    html = template.render(context=new_context)
    # Return the rendered template as safe html
    return jinja2.Markup(html)


@library.global_function
@jinja2.contextfunction
def render_struct(context, struct_value):
    # Use the django_jinja to get the template content based on its name
    template = get_template(struct_value.block.meta.template)
    # Create a new context based on the current one as we can't edit it directly
    new_context = context.get_all()
    # Add the value on the context (value is the keyword chosen by wagtail for the blocks context)
    new_context['value'] = struct_value
    # Render the template with the context
    html = template.render(context=new_context)
    # Return the rendered template as safe html
    return jinja2.Markup(html)


@library.extension
class WagtailSettings(Extension):
    def __init__(self, environment):
        super(WagtailSettings, self).__init__(environment)
        environment.globals['WAGTAIL_SITE_NAME'] = getattr(settings, 'WAGTAIL_SITE_NAME', None)
