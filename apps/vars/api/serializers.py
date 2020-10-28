from django.contrib.sites.models import Site

from rest_framework import serializers

from snippets.api.serializers import fields
from snippets.api.serializers.mixins import CommonSerializer
from vars import models


class MenuSerializer(serializers.ModelSerializer):
    """Меню"""

    items = serializers.SerializerMethodField()

    class Meta:
        model = models.Menu
        fields = ('items', 'slug', 'title')

    @staticmethod
    def get_items(obj):
        items = obj.cached_items \
            if hasattr(obj, 'cached_items') else obj.items.published()

        return MenuItemSerializer(items, many=True).data


class MenuItemSerializer(serializers.ModelSerializer):
    """Пункты меню"""

    child_menu = serializers.SerializerMethodField()

    class Meta:
        model = models.MenuItem
        fields = ('child_menu', 'class_name', 'id', 'title', 'url')

    @staticmethod
    def get_child_menu(obj):
        if obj.child_menu_id:
            return MenuSerializer(obj.child_menu).data


class SiteSerializer(serializers.ModelSerializer):
    """Сайты"""

    class Meta:
        model = Site
        fields = ('domain', 'name')


class SiteConfigSerializer(serializers.ModelSerializer):
    """Настройки сайта"""

    copyrights = fields.PretextField()

    class Meta:
        model = models.SiteConfig
        fields = ('copyrights',)


class SettingsSerializer(CommonSerializer):
    """Настройки"""

    menus = MenuSerializer(many=True)
    settings = SiteConfigSerializer()
