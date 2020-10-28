from django.contrib import admin

from modeltranslation.admin import TranslationStackedInline, TranslationAdmin

from snippets.admin import SuperUserDeletableAdminMixin, BaseModelAdmin
from snippets.utils.modeltranslation import get_model_translation_fields
from vars import models


class MenuItemInline(TranslationStackedInline):
    """Пункты меню"""

    extra = 0
    model = models.MenuItem
    fields = models.MenuItem().collect_fields()
    fk_name = 'menu'
    ordering = ('ordering',)
    raw_id_fields = ('child_menu',)
    readonly_fields = ('created', 'updated')
    suit_classes = 'suit-tab suit-tab-items'


@admin.register(models.Menu)
class MenuAdmin(SuperUserDeletableAdminMixin, BaseModelAdmin, TranslationAdmin):
    """Меню"""

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-basic'),
            'fields': models.Menu().collect_fields()
        })
    ]
    inlines = (MenuItemInline,)
    list_display = (
        'slug', 'title', 'work_title', 'is_global', 'status', 'created'
    )
    list_editable = ('status',)
    list_filter = BaseModelAdmin.list_filter + ('is_global',)
    list_select_related = True
    ordering = BaseModelAdmin.ordering + ('slug',)
    search_fields = ['=id', 'slug', 'title'] + [
        'items__%s' % x for x in get_model_translation_fields(models.MenuItem)
    ]
    suit_form_tabs = (
        ('basic', 'Основное'),
        ('items', 'Пункты меню')
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = tuple(self.readonly_fields)
        if request.user.is_superuser:
            return readonly_fields

        return readonly_fields + ('slug', 'work_title')


@admin.register(models.MenuItem)
class MenuItemAdmin(SuperUserDeletableAdminMixin, BaseModelAdmin,
                    TranslationAdmin):
    """Пункты меню отдельной админкой"""

    list_display = ('id', 'title', 'menu', 'status', 'ordering', 'created')
    list_display_links = ('id', 'title')
    list_filter = BaseModelAdmin.list_filter + ('menu',)
    search_fields = ['=id'] + get_model_translation_fields(models.MenuItem)


@admin.register(models.SiteConfig)
class SiteConfigAdmin(TranslationAdmin):
    """Настройки сайта"""
    pass
