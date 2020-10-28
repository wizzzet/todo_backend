from django.db import models

from snippets.admin import SuperUserDeletableAdminMixin
from snippets.models import BaseModel, BasicModel
from solo.models import SingletonModel


class Menu(SuperUserDeletableAdminMixin, BaseModel):
    """Меню"""

    work_title = models.CharField(
        'Рабочий заголовок', max_length=255, db_index=True
    )
    title = models.CharField(
        'Заголовок', max_length=255, blank=True, null=True
    )
    slug = models.SlugField(
        'Алиас', db_index=True,
        help_text='Латинские буквы и цифры, подчеркивание и дефис'
    )
    is_global = models.BooleanField('Глобальное', default=False)

    translation_fields = ('title',)

    class Meta:
        ordering = ('ordering',)
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.work_title


class MenuItem(SuperUserDeletableAdminMixin, BaseModel):
    """Пункт меню"""

    menu = models.ForeignKey(
        Menu, related_name='items', verbose_name='Меню',
        on_delete=models.CASCADE
    )
    title = models.CharField('Заголовок', max_length=255)
    url = models.CharField('Ссылка', max_length=255)
    class_name = models.CharField(
        'CSS-класс для ссылки (а):', blank=True, null=True, max_length=50
    )
    child_menu = models.ForeignKey(
        'vars.Menu', verbose_name='Дочернее меню', related_name='parent_items',
        on_delete=models.SET_NULL, blank=True, null=True
    )

    translation_fields = ('title', 'url')

    class Meta:
        ordering = ('ordering',)
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return f'{self.menu}: {self.title}'


class SiteConfig(BasicModel, SingletonModel):
    """Настройки сайта"""

    copyrights = models.TextField(
        'Копирайт', max_length=1024, blank=True, null=True
    )

    translation_fields = ('copyrights',)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'
