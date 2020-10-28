from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.models import Group

from import_export.admin import ExportMixin
from import_export.formats import base_formats

from snippets.admin import activate, deactivate
from users.forms import UserAdminForm, UserCreationForm
from users import models, import_export


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    pass


@admin.register(models.User)
class UserAdmin(ExportMixin, UserAdmin):
    """Пользователь"""

    actions = UserAdmin.actions + [activate, deactivate]
    add_form = UserCreationForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-basic'),
            'fields': ('is_active', 'username', 'password', 'created', 'updated')
        }),
        ('Персональные данные', {
            'classes': ('suit-tab', 'suit-tab-basic'),
            'fields': ('last_name', 'first_name', 'email', 'phone')
        }),
        ('Важные даты', {
            'classes': ('suit-tab', 'suit-tab-basic'),
            'fields': ('last_login', 'date_joined')
        }),
        ('Права доступа', {
            'classes': ('suit-tab', 'suit-tab-permission'),
            'fields': ('is_staff', 'is_superuser', 'user_permissions')
        })
    )
    form = UserAdminForm
    formats = [
        base_formats.CSV, base_formats.XLS, base_formats.HTML, base_formats.ODS, base_formats.TSV
    ]
    list_display = ('username', 'first_name', 'last_name', 'phone', 'email', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    readonly_fields = ('last_login', 'date_joined', 'created', 'updated')
    resource_class = import_export.UserResource
    search_fields = (
        '=id', 'email', 'first_name', 'last_name', 'phone', 'username'
    )
    suit_form_tabs = (
        ('basic', 'Основное'),
        ('permission', 'Права доступа')
    )

    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        if 'delete_selected' in actions and not request.user.is_superuser:
            del actions['delete_selected']
        return actions
