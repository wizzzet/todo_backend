from smtplib import SMTPException

from authorization.api.serializers import JWTSerializer
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError, APIException
from rest_framework_jwt.compat import get_username_field

from snippets.utils.email import send_trigger_email, send_email


def register_user(serializer, allow_access=False):
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    raw_password = serializer.validated_data['password']

    user = serializer.save()
    user.set_password(raw_password)
    if allow_access:
        user.has_crm_access = True
    user.save()

    send_trigger_email(
        _('New user'), obj=user, fields=user.email_fields
    )

    try:
        send_email(
            'registration',
            [user.email],
            _('User registered on %s') % settings.SITE_NAME,
            params={
                'site': settings.SITE_NAME,
                'site_url': settings.SITE_URL,
                'user': user,
                'password': raw_password
            }
        )
    except (SMTPException, ConnectionError):
        raise APIException(str(
            _('Registration was successful, but could not send a message with a password.')
        ))

    serializer = JWTSerializer(data={
        get_username_field(): user.email,
        'password': raw_password
    })
    if serializer.is_valid():
        authorization_data = serializer.validated_data
    else:
        raise ValidationError(serializer.errors)

    return authorization_data
