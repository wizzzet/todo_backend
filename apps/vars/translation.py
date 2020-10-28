from django.conf import settings

from modeltranslation.decorators import register

from snippets.utils.modeltranslation import BaseTranslationOptions
from vars import models


@register(models.Menu)
class MenuTranslationOptions(BaseTranslationOptions):
    fields = models.Menu.translation_fields
    required_languages = {'default': ()}


@register(models.MenuItem)
class MenuItemTranslationOptions(BaseTranslationOptions):
    fields = models.MenuItem.translation_fields
    required_languages = {settings.DEFAULT_LANGUAGE: ('url',), 'default': ()}


@register(models.SiteConfig)
class SiteConfigTranslationOptions(BaseTranslationOptions):
    fields = models.SiteConfig.translation_fields
    required_languages = {'default': ()}
