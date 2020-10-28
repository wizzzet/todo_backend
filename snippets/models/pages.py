from django.db import models

from snippets.models import BasicModel, LastModMixin
from snippets.models.seo import SEOModelMixin
from snippets.sites import get_default_site_id


class BasePage(SEOModelMixin, LastModMixin, BasicModel):
    """Базовая модель страниц"""

    site = models.OneToOneField(
        'sites.Site', verbose_name='Сайт', on_delete=models.CASCADE, default=get_default_site_id
    )
    title = models.CharField('Заголовок', max_length=255, blank=True, null=True)

    translation_fields = SEOModelMixin.translation_fields + ('title',)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self._meta.verbose_name} ({self.site.name})'
