from django.db.models import Prefetch
from django.http import Http404

from snippets.api.views import PublicViewMixin, BaseRetrieveAPIView
from vars import models
from vars.api import serializers


class SettingsView(PublicViewMixin, BaseRetrieveAPIView):
    """Настройки"""

    serializer_class = serializers.SettingsSerializer

    def get_object(self):
        site_config = models.SiteConfig.get_solo()

        menus = models.Menu.objects.published().filter(is_global=True) \
            .prefetch_related(
                Prefetch(
                    'items',
                    queryset=models.MenuItem.objects.published().select_related('child_menu'),
                    to_attr='cached_items'
                )
            )

        return {
            'menus': menus,
            'settings': site_config
        }
