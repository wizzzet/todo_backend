from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'vars'
    verbose_name = 'Настройки'
