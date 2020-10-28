from django.utils.translation import ugettext_lazy as _

from snippets.enums import StatusEnum


def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


activate.short_description = _('Активировать')


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


deactivate.short_description = _('Деактивировать')


def draft(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.DRAFT)


draft.short_description = _('В черновики')


def hide(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.HIDDEN)


hide.short_description = _('Скрыть')


def publish(modeladmin, request, queryset):
    queryset.update(status=StatusEnum.PUBLIC)


publish.short_description = _('Опубликовать')
