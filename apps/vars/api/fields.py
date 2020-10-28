from rest_framework import serializers

from vars import models
from vars.api.serializers import MenuSerializer


class MenuField(serializers.ReadOnlyField):
    def __init__(self, slug, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        self.slug = slug
        super(MenuField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        menu = models.Menu.objects.published()\
            .filter(slug=self.slug)\
            .first()

        if menu:
            return MenuSerializer(menu, many=False).data

        return None
