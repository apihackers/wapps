from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore.models import Page

from wagtail.contrib.modeladmin.helpers import PagePermissionHelper
from wagtail.contrib.modeladmin.options import WagtailRegisterable


class PageEditAdmin(WagtailRegisterable):
    model = None
    menu_label = None
    menu_icon = None
    menu_order = None
    parent = None
    permission_helper_class = None

    def __init__(self, parent=None):
        """
        Don't allow initialisation unless self.model is set to a valid model
        """
        if not self.model or not issubclass(self.model, Page):
            raise ImproperlyConfigured(
                u"The model attribute on your '%s' class must be set, and "
                "must be a valid Django model." % self.__class__.__name__)
        self.opts = self.model._meta
        self.parent = parent
        permission_helper_class = self.get_permission_helper_class()
        self.permission_helper = permission_helper_class(self.model)

    def get_permission_helper_class(self):
        if self.permission_helper_class:
            return self.permission_helper_class
        return PagePermissionHelper

    def get_page(self):
        return self.model._default_manager.get_queryset().first()

    def get_menu_label(self):
        """
        Returns the label text to be used for the menu item
        """
        return self.menu_label or self.opts.verbose_name_plural.title()

    def get_menu_icon(self):
        """
        Returns the icon to be used for the menu item. The value is prepended
        with 'icon-' to create the full icon class name. For design
        consistency, the same icon is also applied to the main heading for
        views called by this class
        """
        if self.menu_icon:
            return self.menu_icon
        return 'doc-full-inverse'

    def get_menu_order(self):
        """
        Returns the 'order' to be applied to the menu item. 000 being first
        place. Where ModelAdminGroup is used, the menu_order value should be
        applied to that, and any ModelAdmin classes added to 'items'
        attribute will be ordered automatically, based on their order in that
        sequence.
        """
        return self.menu_order or 999

    def show_menu_item(self, request):
        """
        Returns a boolean indicating whether the menu item should be visible
        for the user in the supplied request, based on their permissions.
        """
        return self.permission_helper.can_edit_object(request.user, self.get_page())

    def get_admin_urls_for_registration(self):
        return tuple()

    def get_menu_item(self, order=None):
        """
        Utilised by Wagtail's 'register_menu_item' hook to create a menu item
        to access the listing view, or can be called by ModelAdminGroup
        to create a SubMenu
        """
        return MenuItem(
            self.get_menu_label(),
            self.get_menu_url(),
            classnames='icon icon-%s' % self.get_menu_icon(),
            order=order or self.get_menu_order()
        )

    def get_menu_url(self):
        page = self.get_page()
        if page:
            return reverse('wagtailadmin_pages:edit', args=(page.pk, ))


class PageExploreAdmin(PageEditAdmin):
    def get_menu_url(self):
        page = self.get_page()
        if page:
            return reverse('wagtailadmin_explore', args=(page.pk, ))
