from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'

    menu = [
        ParentItem(
            'Настройки',
            children=[
                ChildItem(model='vars.menu'),
                ChildItem(model='vars.menuitem'),
                ChildItem(model='vars.siteconfig')
            ]
        ),
        ParentItem(
            'Пользователи',
            children=[
                ChildItem(model='users.user'),
                ChildItem(model='auth.group')
            ]
        )
    ]
