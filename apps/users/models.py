from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from snippets.models import LastModMixin, BasicModel
from users.managers import UserManager


class User(AbstractUser, LastModMixin, BasicModel):
    """Пользователь"""

    REQUIRED_FIELDS = ['email']

    email = models.EmailField('Email', unique=True)
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)

    email_verified_date = models.DateTimeField(
        'Дата и время подтверждения email', blank=True, null=True
    )
    restore_salt = models.CharField(
        'Соль восстановления пароля', max_length=80,
        help_text='Выставляется при запросе восстановления пароля и удаляется '
                  'после успешной смены пароля, либо по сроку годности',
        blank=True, null=True
    )
    restore_salt_expiry = models.DateTimeField(
        'Срок годности соли восстановления', blank=True, null=True
    )
    restore_token = models.CharField(
        'Токен восстановления пароля', max_length=80,
        help_text='Выставляется при подтверждении email\'а запроса '
                  'восстановления пароля. Удаляется после успешной смены '
                  'пароля, либо по сроку годности',
        blank=True, null=True
    )
    restore_token_expiry = models.DateTimeField(
        'Срок годности токена восстановления', blank=True, null=True
    )

    email_fields = ('email', 'first_name', 'last_name', 'username')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        parts = map(
            lambda x: x.strip(),
            filter(None, (self.last_name, self.first_name))
        )
        full_name = ' '.join(parts)

        return full_name or self.username

    get_full_name.short_description = 'ФИО'
    get_full_name.admin_order_field = 'full_name'
