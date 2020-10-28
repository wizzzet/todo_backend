from django.db import models
from django.utils.translation import ugettext_lazy as _

from solo.models import SingletonModel

from snippets.enums import PaymentStatusEnum
from snippets.models import LastModMixin, BasicModel
from snippets.models.seo import SEOModelMixin


class BasePage(SEOModelMixin, LastModMixin, BasicModel, SingletonModel):
    """Base page model"""
    title = models.CharField(_('Заголовок'), max_length=255, blank=True, null=True)

    translation_fields = ('title',)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class BasePayment(models.Model):
    total_amount = models.DecimalField(
        _('Total amount'), blank=True, max_digits=11, decimal_places=2
    )

    payment_gateway_order_id = models.CharField(
        _('Payment gateway ID'), blank=True, null=True, max_length=64
    )
    income = models.DecimalField(
        _('Received amount'), max_digits=11, decimal_places=2, blank=True, null=True
    )
    payment_status = models.SmallIntegerField(
        _('Payment status'), choices=PaymentStatusEnum.get_choices(),
        default=PaymentStatusEnum.default
    )

    payment_error_code = models.CharField(
        _('Payment error code'), max_length=20, blank=True, null=True
    )
    payment_error_message = models.TextField(
        _('Payment error text'), blank=True, null=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def get_payment_id(self):
        return self.pk
