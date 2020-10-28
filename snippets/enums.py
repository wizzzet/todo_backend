from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _

from snippets.models import BaseEnumerate


class PaymentStatusEnum(BaseEnumerate):
    """ Статусы оплаты """
    NOT_PAID = -1
    PAID = 1

    values = OrderedDict((
        (NOT_PAID, _('Не оплачено')),
        (PAID, _('Оплачено'))
    ))

    default = NOT_PAID


class StatusEnum(BaseEnumerate):
    """
    Object publicity status enumerate
    """
    DRAFT = 0
    PUBLIC = 1
    HIDDEN = 2

    values = OrderedDict((
        (DRAFT, _('Черновик')),
        (PUBLIC, _('Публичный')),
        (HIDDEN, _('Скрытый')),
    ))
